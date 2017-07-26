import boto3
import json
import logging
import os
import re
import urllib
import urllib2
import hashlib
import base64
import time
from urlparse import urlparse, parse_qs
from botocore.exceptions import ClientError
from PIL import Image, ImageDraw

from backend.env import *
from backend.slack import *
from backend.image import create_location_image

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb_client = boto3.client('dynamodb')
s3_client = boto3.client('s3')

def respond(err, res=None):
    logger.info("[response to slack] " + res)
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def query_location(locationName):
    locationName = locationName.lower()
    response = dynamodb_client.get_item(
        TableName=LOCATIONS_TABLE_NAME,
        Key= {
            "entityName": {
                "S": locationName
            }
        }
    )
    logger.info("[response from location query] " + json.dumps(response))
    if (u"Item" in response):
        return True, {
            "location_x": float(response[u"Item"][u"x"][u"S"]),
            "location_y": float(response[u"Item"][u"y"][u"S"]),
            "floor": response[u"Item"][u"floor"][u"S"],
            "created_by": response[u"Item"][u"createdby"][u"S"],
            "created_on": response[u"Item"][u"createdon"][u"S"]
        }
    else:
        return False, {}

def query_auth(user_id):
    response = dynamodb_client.get_item(
        TableName=AUTH_TABLE_NAME,
        Key= {
            "user_id": {
                "S": user_id
            }
        }
    )
    logger.info("[response from auth query] " + json.dumps(response))
    if (u"Item" in response):
        return True, response[u"Item"][u"access_token"][u"S"]
    else:
        return False, {}

def getDisplayName(locationName):
    p = re.compile(r'<(.).*?\|(.*?)>')
    display_name = p.sub(r'\1\2', locationName)
    return display_name.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")

def create_change_url(locationName, requesterUserId, requesterUserName):
    data = {
        "url": link_to_db_helper,
        "name": getDisplayName(locationName),
        "createdBy" : "<@" + requesterUserId + "|" + requesterUserName + ">",
        "locationName": locationName
    }
    return link_to_frontend + "?data=" + base64.urlsafe_b64encode(json.dumps(data))

def create_image(locationName, location_x, location_y, floor):
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

    return "https://s3.amazonaws.com/" + bucket + "/" + filename

def create_and_upload_image(responseText, _):
    try:
        locationName = responseText[u"text"][0]
        requesterUserName = responseText[u"user_name"][0]
        requesterUserId = responseText[u"user_id"][0]
        in_channel = responseText[u"channel_id"][0]
    except KeyError:
        return respond(None, create_failed_slack_response("Are you sure this message was sent from Slack?"))

    is_authenticated, access_token = query_auth(requesterUserId)
    if not is_authenticated:
        return respond(None, create_slack_auth_response(slack_client_id, link_to_db_helper, team_id))

    change_url = create_change_url(locationName, requesterUserId, requesterUserName)
    locationExists, db_results = query_location(locationName)
    if locationExists:
        image_url = create_image(locationName, db_results["location_x"], db_results["location_y"], db_results["floor"])
        response = create_slack_response(in_channel, locationName, image_url, change_url, db_results["created_by"], db_results["created_on"], access_token)
        return respond(None, response)
    else:
        response = create_slack_response_not_found(locationName, change_url)
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

def main(event, context):
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
