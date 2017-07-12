import boto3
import json
import logging
import os

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

def lambda_handler(event, context):
    # logger.info("event:" + str(event))
    # logger.info("context:" + str(context))

    # location = event[u"entityName"]
    # x = event[u"x"]
    # y = event[u"y"]

    # dynamodb_client.put_item(
    #   TableName="Locations",
    #   Item={
    #     "entityName": {
    #       "S": location
    #     },
    #       "x": {
    #         "S": str(x)
    #       },
    #       "y": {
    #         "S": str(y)
    #       }
    #     }
    # )
    body = "<html><head><title>HTML from API Gateway/Lambda</title></head><body><h1><font color=\"red\">HTML from API Gateway/Lambda</h1></body></html>"
    return {
        'statusCode': '200',
        'body': body,
        'headers': {
            'Content-Type': 'text/html',
        },
    }

    return respond(None, "Yay it worked")