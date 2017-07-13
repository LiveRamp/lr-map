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
    # logger.info("event:" + str(event))
    # logger.info("context:" + str(context))
    text = str(event)
    text = text.split("?")[1:4]
    location = text[0]
    x = text[1]
    y = text[2]


    add_to_db(location, x, y)
    reply = 'var result = { success: true, text : "' + str(text) + '" }'
    return respond(None, reply)
    # return respond(None, str(event) + str(context))

    # body = event[u"body"]
    # jsonDict = json.loads(body)

    # htmlFile = '''
    # <html>
    #   <head>
    #     <meta name="viewport" content="width=device-width, minimum-scale=0.1">
    #     <title>16th.png (2584x1293)</title>
    #     <script src='index.js'></script>
    #   <link rel="stylesheet" type="text/css" href="style.css">
    #   <link href="https://fonts.googleapis.com/css?family=Source+Code+Pro" rel="stylesheet">
    #   <script src="https://use.fontawesome.com/0bdbe2307d.js"></script>
    #   <script src="https://cdn.rawgit.com/alertifyjs/alertify.js/v1.0.10/dist/js/alertify.js"></script>
    #   <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    #   </head>
    #   <body>
    #     <iframe style="height:100%;width:100%;" frameBorder="0" src="http://mapsstatic.s3-website-us-east-1.amazonaws.com/"></iframe>
    #   </body>
    # </html>
    # '''
    # htmlFile = '''
    # var test = function() {
    #      axios.post('https://1aw7zewd9c.execute-api.us-east-1.amazonaws.com/prod/addToMapDb', {
    #         entityName: "test",
    #         x: "0.5",
    #         y: "0.5"
    #       });
    # }
    # '''

    # return {
    #     'statusCode': '200',
    #     'body': htmlFile,
    #     'headers': {
    #         'Content-Type': 'text/html',
    #     },
    # }

    # location = jsonDict["entityName"]
    # x = event["x"]
    # y = event["y"]
    # return (None, str(event))

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
    # body = "<html><head><title>HTML from API Gateway/Lambda</title></head><body><h1><font color=\"red\">HTML from API Gateway/Lambda</h1></body></html>"
    # return {
    #     'statusCode': '200',
    #     'body': body,
    #     'headers': {
    #         'Content-Type': 'text/html',
    #     },
    # }

    # return respond(None, "Yay it worked" + str(jsonDict))
    # return respond(None, "Yay it worked")