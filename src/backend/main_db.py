import boto3
import json
import logging
import os

import urllib
import urllib2
import ast
import time
import base64
from backend.env import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb_client = boto3.client('dynamodb')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def add_to_locations(entityName, created_by, x, y, floor):
    entityName = entityName.lower()
    dynamodb_client.put_item(
        TableName=LOCATIONS_TABLE_NAME,
        Item={
            "entityName": {
                "S": entityName
            },
            "createdby": {
                "S": str(created_by)
            },
            "createdon": {
                "S": str(int(round(time.time())))
            },
            "x": {
                "S": str(x)
            },
            "y": {
                "S": str(y)
            },
            "floor": {
                "S": str(floor)
            }
        }
    )

def handle_location(event):
    eventData = event[u"queryStringParameters"][u"data"]
    logger.info("eventData:")
    logger.info(eventData)

    toUtf = eventData.encode('UTF-8')
    logger.info("toUtf:")
    logger.info(toUtf)

    decoded = base64.urlsafe_b64decode(toUtf)
    logger.info("decoded:")
    logger.info(decoded)

    data = json.loads(decoded)
    logger.info("data:")
    logger.info(data)

    x = event[u"queryStringParameters"][u"x"]
    y = event[u"queryStringParameters"][u"y"]
    floor = event[u"queryStringParameters"][u"floor"]
    location = data["locationName"]
    created_by = data["createdBy"]

    add_to_locations(location, created_by, x, y, floor)

    textreply = str((location, created_by, x, y, floor))

    reply = 'var result = { success: true }'
    return respond(None, reply)


def add_to_auth(user_id, access_token):
    dynamodb_client.put_item(
        TableName=AUTH_TABLE_NAME,
        Item={
            "user_id": {
                "S": user_id
            },
            "access_token": {
                "S": access_token
            },
        }
    )
    
def handle_auth(event):
    code = event[u"queryStringParameters"][u"code"]
    url = "https://slack.com/api/oauth.access"
    params = urllib.urlencode({
        "client_id": slack_client_id,
        "client_secret" : slack_client_secret,
        "code" : code,
        "redirect_uri" : link_to_db_helper,
        })
    response = urllib2.urlopen(url, params).read()
    logger.info("[auth request response] " + response)
    response = json.loads(response)
    if response["ok"] == True:
        add_to_auth(response["user_id"], response["access_token"])
        return respond(None, "Great success!")
    else:
        logger.error("[error during auth]")
        return respond(None, "There was an error.")


def main(event, context):
    logger.info("[event] " + json.dumps(event))
    if u"code" in event[u"queryStringParameters"]:
        return handle_auth(event)
    else:
        return handle_location(event)
