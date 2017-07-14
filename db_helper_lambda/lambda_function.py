import boto3
import json
import logging
import os

import urllib
import ast
import time

LOCATIONS_TABLE_NAME = "MapLocations"

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

def add_to_db(entityName, created_by, x, y, floor):
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

def lambda_handler(event, context):
    data = json.loads(urllib.unquote(event[u"queryStringParameters"][u"data"]))
    x = event[u"queryStringParameters"][u"x"]
    y = event[u"queryStringParameters"][u"y"]
    floor = event[u"queryStringParameters"][u"floor"]
    location = data["locationName"]
    created_by = data["expandedUserName"]

    add_to_db(location, created_by, x, y, floor)

    textreply = str((location, created_by, x, y, floor))

    reply = 'var result = { success: true, text:  "' + textreply  +  '" }'
    return respond(None, reply)
