import boto3
import json
import logging
import os

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

LOCATIONS_TABLE_NAME = "MapLocations"

dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')

if "PROD" in os.environ:
  link_to_frontend = "http://***REMOVED***.s3-website-us-east-1.amazonaws.com/"
  bucket = "slack-map-images"
elif "TEST" in os.environ:
  link_to_frontend = "http://***REMOVED***-test.s3-website-us-east-1.amazonaws.com/"
  bucket = "slack-map-images-test"
else:
  sys.exit(1)

def respond(err, res=None):
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
  logger.info("Response: " + str(response))

  # TODO: react if the conference room is missing
  return {
      "location_x": float(response[u"Item"][u"x"][u"S"]),
      "location_y": float(response[u"Item"][u"y"][u"S"]),
      "floor": response[u"Item"][u"floor"][u"S"],
      "created_by": response[u"Item"][u"createdby"][u"S"],
      "created_on": response[u"Item"][u"createdon"][u"S"]
  }

def create_and_upload_image(responseText, _):
    try:
        locationName = responseText[u"text"][0]
        requesterUserName = responseText[u"user_name"][0]
        requesterUserId = responseText[u"user_id"][0]
        in_channel = responseText[u"channel_id"][0]
    except KeyError:
        return respond(None, create_failed_slack_response("Are you sure this message was sent from Slack?"))

    escapedLocationName = urllib.quote(locationName)

    if locationName.startswith("<"):
      display_name = locationName[1] + locationName.split('|')[1][:-1]
    else:
      display_name = locationName

    expandedUserName = "<@" + requesterUserId + "|" + requesterUserName + ">"
    data = {
        "name": display_name,
        "expandedUserName" : expandedUserName,
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

    response = create_slack_response(in_channel, locationName, image_url, change_url, created_by, created_on)
    logger.info(response)
    return respond(None, response)

def interactive_action (responseText, action):
    url = 'https://slack.com/api/chat.postMessage'
    text = "text"
    if action == "send":
        payload = responseText[u"payload"][0]

        jsonDict = json.loads(payload)
        value = jsonDict[u"actions"][0]["value"]
        logger.info("value:")
        value = base64.urlsafe_b64decode(value.encode("UTF-8"))
        logger.info(value)
        response = urllib2.urlopen(url, data=value).read()
        if json.loads(response)["ok"] == False:
            logger.error("Error during post message: " + str(response))

    return respond(None, '{ "delete_original" : "true" }')

def lambda_handler(event, context):
    logger.info("Looks like autoamtic deployment works. event: " + str(event))
    data = event[u"body"]
    responseText = parse_qs(data)
    logger.info("responseText: " + str(responseText))

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

