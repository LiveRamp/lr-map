import boto3
import json
import logging
import os

import urllib
import ast

LOCATIONS_TABLE_NAME = "Locations"

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

def add_to_db(entityName, createdBy, x, y, room):
    dynamodb_client.put_item(
      TableName="Locations",
      Item={
        "entityName": {
          "S": entityName
        },
          "createdby": {
            "S": str(createdBy)
          },
          "x": {
            "S": str(x)
          },
          "y": {
            "S": str(y)
          },
          "room": {
            "S": str(room)
          }
        }
    )

def lambda_handler(event, context):
    location = event[u"queryStringParameters"][u"name"]
    createdBy = event[u"queryStringParameters"][u"createdby"]
    x = event[u"queryStringParameters"][u"x"]
    y = event[u"queryStringParameters"][u"y"]
    room = event[u"queryStringParameters"][u"room"]

    add_to_db(location, createdBy, x, y, room)

    reply = 'var result = { success: true, text:  "' + str((location, createdBy, x, y, room))  +  '" }'
    return respond(None, reply)
