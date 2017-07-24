import boto3
import json
import logging
import os
import re

import base64
import os

from PIL import Image, ImageDraw
import time
import urllib2

from slack import create_slack_response, create_failed_slack_response, create_slack_response_not_found, create_send_slack_message
from image import create_location_image

from botocore.exceptions import ClientError

import urllib
import hashlib
from urlparse import urlparse, parse_qs
import sys


logger = logging.getLogger()
logger.setLevel(logging.INFO)

locations = {
  "Dominion": (0.1, 0.6),
  "Center": (0.5, 0.5),
  "Corner": (0.85, 0.85)
}

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')

if "PROD" in os.environ:
  link_to_frontend = "http://***REMOVED***.s3-website-us-east-1.amazonaws.com/"
  link_to_db_helper = 'https://hbe9t0i30j.execute-api.us-east-1.amazonaws.com/prod/***REMOVED***-db-helper'
  bucket = "slack-map-images"
  token = "xoxp-76626825879-169433398609-213106662900-ff609783bfac5a5a8dac32618a941c0b"
  LOCATIONS_TABLE_NAME = "MapLocations"
elif "TEST" in os.environ:
  link_to_frontend = "http://***REMOVED***-staging.s3-website-us-east-1.amazonaws.com/"
  link_to_db_helper = 'https://***REMOVED***.execute-api.us-east-1.amazonaws.com/prod/***REMOVED***-db-helper-staging'
  bucket = "***REMOVED***"
  token = "xoxp-113070057776-211135045057-212852625397-a02dc2cae27533deca6f9583815fe60f"
  LOCATIONS_TABLE_NAME = "MapLocationsStaging"
else:
  sys.exit(1)

def respond(err, res=None):
    logger.info("[response to slack] " + res)
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def query_db(locationName):
  response = dynamodb_client.get_item(
    TableName=LOCATIONS_TABLE_NAME,
    Key= {
      "entityName": {
        "S": locationName
      }
    }
  )
  logger.info("[response from db] " + json.dumps(response))

  # TODO: react if the conference room is missing
  return {
      "location_x": float(response[u"Item"][u"x"][u"S"]),
      "location_y": float(response[u"Item"][u"y"][u"S"]),
      "floor": response[u"Item"][u"floor"][u"S"],
      "created_by": response[u"Item"][u"createdby"][u"S"],
      "created_on": response[u"Item"][u"createdon"][u"S"]
  }

def getDisplayName(locationName):
    p = re.compile(r'<(.).*?\|(.*?)>')
    display_name = p.sub(r'\1\2', locationName)
    return display_name.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


def create_and_upload_image(responseText, _):
    try:
        locationName = responseText[u"text"][0]
        requesterUserName = responseText[u"user_name"][0]
        requesterUserId = responseText[u"user_id"][0]
        in_channel = responseText[u"channel_id"][0]
    except KeyError:
        return respond(None, create_failed_slack_response("Are you sure this message was sent from Slack?"))

    data = {
        "url": link_to_db_helper,
        "name": getDisplayName(locationName),
        "createdBy" : "<@" + requesterUserId + "|" + requesterUserName + ">",
        "locationName": locationName
    }
    change_url = link_to_frontend + "?data=" + base64.urlsafe_b64encode(json.dumps(data))

    try:
      db_results = query_db(locationName)
      for key, val in db_results.items():
        exec(key + '=val')
    except Exception as e:
      response = create_slack_response_not_found(locationName, change_url)
      return respond(None, response)

    escapedLocationName = urllib.quote(locationName)
    md5 = hashlib.md5()
    md5.update(escapedLocationName)
    filename = str(md5.hexdigest()) + "_" + str(time.strftime("%H:%M:%S")) + ".gif"
    filepath = "/tmp/" + filename

    try:
      s3_client.head_object(Bucket=bucket, Key=filename)
      logger.info("The file already exists, so a new one will not be created.")
    except ClientError as e:
      logger.info("Creating the file because of the error: " + str(e))
      create_location_image(location_x, location_y, filepath, floor)
      s3_client.upload_file(filepath, bucket, filename)

    image_url =  "https://s3.amazonaws.com/" + bucket + "/" + filename

    response = create_slack_response(in_channel, locationName, image_url, change_url, created_by, created_on, token)
    return respond(None, response)

def interactive_action (responseText, action):
    url = 'https://slack.com/api/chat.postMessage'
    text = "text"
    if action == "send":
        payload = responseText[u"payload"][0]

        jsonDict = json.loads(payload)
        value = jsonDict[u"actions"][0]["value"]
        value = base64.urlsafe_b64decode(value.encode("UTF-8"))
        logger.info("[send value] " + json.dumps(value))
        response = urllib2.urlopen(url, data=value).read()
        if json.loads(response)["ok"] == False:
            logger.error("Error during post message: " + str(response))

    return respond(None, '{ "delete_original" : "true" }')

def lambda_handler(event, context):
    logger.info("[event] " + json.dumps(event))
    data = event[u"body"]
    responseText = parse_qs(data)
    logger.info("[parsed event] " + json.dumps(responseText))

    if "action_ts" in str(event):
      if "send8037123" in str(event):
        action = "send"
      elif "cancel8037123" in str(event):
        action = "cancel"
      else:
        logger.error("Unknown action.")
      request_type = "interactive_action"
    else:
      action = "fetch_image"
      request_type = "create_and_upload_image"

    request_type_to_action = {
            "create_and_upload_image": create_and_upload_image,
            "interactive_action": interactive_action
            }

    return request_type_to_action[request_type](responseText, action)

