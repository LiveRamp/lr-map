'''
This function handles a Slack slash command and echoes the details back to the user.

Follow these steps to configure the slash command in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new

  2. Search for and select "Slash Commands".

  3. Enter a name for your command and click "Add Slash Command Integration".

  4. Copy the token string from the integration settings and use it in the next section.

  5. After you complete this blueprint, enter the provided API endpoint URL in the URL field.


To encrypt your secrets use the following steps:

  1. Create or use an existing KMS Key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html

  2. Click the "Enable Encryption Helpers" checkbox

  3. Paste <COMMAND_TOKEN> into the kmsEncryptedToken environment variable and click encrypt


Follow these steps to complete the configuration of your command API endpoint

  1. When completing the blueprint configuration select "Open" for security
     on the "Configure triggers" page.

  2. Enter a name for your execution role in the "Role name" field.
     Your function's execution role needs kms:Decrypt permissions. We have
     pre-selected the "KMS decryption permissions" policy template that will
     automatically add these permissions.

  3. Update the URL for your Slack slash command with the invocation URL for the
     created API resource in the prod stage.
'''

import boto3
import json
import logging
import os

from base64 import b64decode
from urlparse import parse_qs
import os

import json


#ENCRYPTED_EXPECTED_TOKEN = os.environ['kmsEncryptedToken']

#kms = boto3.client('kms')#
#expected_token = kms.decrypt(CiphertextBlob=b64decode(ENCRYPTED_EXPECTED_TOKEN))['Plaintext']

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


def lambda_handler(event, context):
    # params = parse_qs(event['body'])
    #token = params['token'][0]
    # if token != expected_token:
        # logger.error("Request token (%s) does not match expected", token)
        # return respond(Exception('Invalid request token'))

    #user = params['user_name'][0]
    #command = params['command'][0]
    #channel = params['channel_name'][0]
    #command_text = params['text'][0]

    # data = json.loads(event, encoding=)
    # json.JSONDecoder.decode(event)
    arguments = event[u'queryStringParameters'][u'text']

    argumentsInt = int(arguments)
    



    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')

    bucket = "maps42"
    filename = "newfile.txt"
    filepath = "/tmp/" + filename
    file = open(filepath, 'w+')
    file.write("abc")
    s3_client.upload_file('/tmp/newfile.txt', bucket, filename)

    image_url = "https://s3.amazonaws.com/maps42/example_file.png"
    title = "Something something"
    text = str(arguments)

    response = {
        "response_type": "ephemeral",
        "text": text,
        "attachments": [
            {
                "title": title,
                "image_url": image_url,
                "color": "#764FA0"
            }
        ]
    }
    return respond(None, response)
    #return respond(None, "Hello world!")
    #return respond(None, "%s invoked %s in %s with the following text: %s" % (user, command, channel, command_text))