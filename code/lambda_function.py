import boto3
import json
import logging
import os

from base64 import b64decode
import os

from PIL import Image, ImageDraw
import time

from slack import create_slack_response, create_failed_slack_response, create_slack_response_not_found
from image import create_location_image

from botocore.exceptions import ClientError

import urllib
import hashlib
from urlparse import urlparse, parse_qs


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

def create_and_upload_image(responseText):
    try:
        locationName = responseText[u"text"][0]
        requesterUserName = responseText[u"user_name"][0]
        requesterUserId = responseText[u"user_id"][0]
    except KeyError:
        return respond(None, create_failed_slack_response("Are you sure this message was sent from Slack?"))

    escapedLocationName = urllib.quote(locationName)

    link_to_frontend = "http://***REMOVED***.s3-website-us-east-1.amazonaws.com/"
    expandedUserName = "<@" + requesterUserId + "|" + requesterUserName + ">"

    data = {
      "expandedUserName" : expandedUserName,
      "locationName": locationName
    }

    if locationName.startswith("<"):
      display_name = locationName[1] + locationName.split('|')[1][:-1]
    else:
      display_name = locationName
    change_url = link_to_frontend + "?name=" + urllib.quote(display_name) + "&data=" + urllib.quote(json.dumps(data))

    try:
      db_results = query_db(locationName)
      for key, val in db_results.items():
        exec(key + '=val')
    except Exception as e:
      response = create_slack_response_not_found(locationName, change_url)
      return respond(None, response)

    bucket = "slack-map-images"
    md5 = hashlib.md5()
    md5.update(escapedLocationName)
    filename = str(md5.hexdigest()) + "_" + str(time.strftime("%H:%M:%S")) + ".gif"
    filepath = "/tmp/" + filename

    try:
      s3_client.head_object(Bucket=bucket, Key=filename)
      logger.info("The file already exists, so a new one will not be created.")
    except ClientError as e:
      logger.info("Creating the file because of the error: " + str(e))
      create_location_image(location_x, location_y, filepath)
      s3_client.upload_file(filepath, bucket, filename)

    image_url =  "https://s3.amazonaws.com/" + bucket + "/" + filename

    response = create_slack_response(locationName, image_url, change_url, created_by, created_on)
    return respond(None, response)

def interactive_action (responseText):
    action = "cancel" #<todo tomasz>
    return respond(None, create_failed_slack_response("{}"))


def lambda_handler(event, context):
    logger.info("Looks like autoamtic deployment works. event: " + str(event))
    data = event[u"body"]
    responseText = parse_qs(data)

    # request_type = "interactive_action" #<todo tomasz>
    # request_type = "create_and_upload_image" #<todo tomasz>

    if "payload" in str(event):
      request_type = "interactive_action"
    else:
      request_type = "create_and_upload_image"

    # request_type = "create_and_upload_image"


    request_type_to_action = {
            "create_and_upload_image": create_and_upload_image,
            "interactive_action": interactive_action
            }

    return request_type_to_action[request_type](responseText)

