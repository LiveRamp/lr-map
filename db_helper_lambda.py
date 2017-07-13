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

def add_to_db(entityName, x, y):
    dynamodb_client.put_item(
      TableName="Locations",
      Item={
        "entityName": {
          "S": entityName
        },
          "x": {
            "S": str(x)
          },
          "y": {
            "S": str(y)
          }
        }
    )

def lambda_handler(event, context):
    location = event[u"queryStringParameters"][u"name"]
    x = event[u"queryStringParameters"][u"x"]
    y = event[u"queryStringParameters"][u"y"]

    add_to_db(location, x, y)

    reply = 'var result = { success: true, text:  "' + str((location, x, y))  +  '" }'
    return respond(None, reply)
