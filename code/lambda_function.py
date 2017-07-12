import boto3
import json
import logging
import os

from base64 import b64decode
from urlparse import parse_qs
import os

from PIL import Image, ImageDraw
import time

from slack import create_slack_response, create_failed_slack_response
from image import create_location_image

from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

locations = {
  "Dominion": (0.1, 0.6),
  "Center": (0.5, 0.5),
  "Corner": (0.85, 0.85)
}

dynamodb_client = boto3.client('dynamodb')

def insert_hardcoded_into_db():
  for location in locations:
    (x, y) = locations[location]
    dynamodb_client.put_item(
      TableName="Locations",
      Item={
        "entityName": {
          "S": location
        },
          "x": {
            "S": str(x)
          },
          "y": {
            "S": str(y)
          }
        }
    )

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def get_location(locationName):
  response = dynamodb_client.get_item(
    TableName="Locations",
    Key= {
      "entityName": {
        "S": locationName
      }
    }
  )
  logger.info("Response: " + str(response))

  # TODO: react if the conference room is missing
  location_x = float(response[u"Item"][u"x"][u"S"])
  location_y = float(response[u"Item"][u"y"][u"S"])

  return (float(response[u"Item"][u"x"][u"S"]), float(response[u"Item"][u"y"][u"S"]))

def create_and_upload_image(event, context):
    insert_hardcoded_into_db()

    try:
        locationName = event[u'queryStringParameters'][u'text']
    except KeyError:
        return respond(None, create_failed_slack_response("Are you sure this message was sent from Slack?"))

    # TODO: react if the conference room is missing
    location_x, location_y = get_location(locationName)


    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')

    bucket = "maps42"
    filename = locationName + str(time.strftime("%H:%M")) + ".gif"
    filepath = "/tmp/" + filename

    try:
      s3_client.head_object(Bucket=bucket, Key=filename)
      logger.info("The file already exists, so a new one will not be created.")
    except ClientError as e:
      logger.info("Creating the file because of the error: " + str(e))
      create_location_image(location_x, location_y, filepath)
      s3_client.upload_file(filepath, bucket, filename)

    image_url =  "https://s3.amazonaws.com/maps42/" + filename

    response = create_slack_response("Tomasz", image_url, locationName)
    return respond(None, response)


def lambda_handler(event, context):

    request_type = "create_and_upload_image" #<todo tomasz>

    request_type_to_action = {
            "create_and_upload_image": create_and_upload_image
            }

    return request_type_to_action[request_type](event, context)
