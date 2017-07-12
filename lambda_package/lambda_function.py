import boto3
import json
import logging
import os

from base64 import b64decode
from urlparse import parse_qs
import os

from PIL import Image, ImageDraw
import time

from slack import create_slack_response


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def respond(err, res=None):
    return {
            'statusCode': '400' if err else '200',
            'body': err.message if err else json.dumps(res),
            'headers': {
                'Content-Type': 'application/json',
                },
            }

def create_and_upload_image(event, context):
    # arguments = event[u'queryStringParameters'][u'text']
    # argumentsInt = int(arguments)
    location_x = 0.5
    location_y = 0.5

    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')

    bucket = "maps42"
    filename = "newfile" + str(time.strftime("%H:%M:%S")) + ".gif"
    filepath = "/tmp/" + filename
    create_location_image(location_x, location_y, filepath)
    s3_client.upload_file(filepath, bucket, filename)

    image_url =  "https://s3.amazonaws.com/maps42/" + filepath

    response = create_slack_response("Tomasz", image_url)
    return respond(None, response)


def lambda_handler(event, context):

    request_type = "create_and_upload_image" #<todo tomasz>

    request_type_to_action = {
            "create_and_upload_image": create_and_upload_image
            }

    return request_type_to_action[request_type](event, context)
