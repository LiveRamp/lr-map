# liveramp_map
This app lets you use **/map** in Slack to find and share the location of meeting rooms, people or anything else.

## Technical Overview
The app heavily uses different [AWS](https://aws.amazon.com/) services, namely: [Lambda](https://aws.amazon.com/lambda/), [S3](https://aws.amazon.com/s3/) and [DynamoDB](https://aws.amazon.com/dynamodb/). To get access to AWS please follow this [guide](https://support.liveramp.com/display/CI/Log+in+to+AWS+console).

The [production app](https://api.slack.com/apps/A66HG571D) is replicated in a staging environment. The [staging app] enables (https://api.slack.com/apps/A69HPA27R) testing via the [AcxiomSandbox](acxiom-sandbox.slack.com) Slack team. In the following everything will be described in terms of production, staging is identical except the services have **-staging** appended. 

There are two lambdas the [app lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/***REMOVED***?tab=code) takes care of all the slack interactions. The [db lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/***REMOVED***-db-helper?tab=code) is used for database entry. They are located at [src/backend/main_app.py](https://git.liveramp.net/MasterRepos/liveramp_map/blob/master/src/backend/main_app.py) and [src/backend/main_db.py](https://git.liveramp.net/MasterRepos/liveramp_map/blob/master/src/backend/main_db.py).

The static content ist stored in two buckets on S3. The [static content bucket](https://s3.console.aws.amazon.com/s3/buckets/***REMOVED***/?region=us-east-1&tab=overview) is used for hosting the website and the [image bucket](https://s3.console.aws.amazon.com/s3/buckets/slack-map-images/?region=us-east-1&tab=overview) is used to store and serve the resulting gifs.

There are two tables in DynamoDB. The [MapLocations table](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=MapLocations) contains all the location data and the [AuthTokens table](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=AuthTokens) contains the access tokens which enable the app to send messages on behalve of the user.

## Technical Details

It is recommended that you read the [usage guide](https://support.liveramp.com/display/CI/Find+and+share+locations+of+meeting+rooms+and+people%27s+desks) before continuing.

### Slack access_token

The first step every user has to complete is to give the app the rights to send messages as the user. This is important since we can not send messages in direct messages otherwise. Please refer to the [Slack documentation](https://api.slack.com/docs/oauth) for how the authentication works.

The first request the user sends is processed by main_app.py. It checks if the AuthTokens table contains a access_token for this user's id. If this is not the case a Slack message is returned which contains a link to the slack authentication url (`https://slack.com/oauth/authorize?`) with all the neccesary parameters. After the user clicks the Authorize button he is redirected to the url specified in the [OAuth & Permissions section](https://api.slack.com/apps/A66HG571D/oauth) of the Slack app. This url points to the main_db lambda which finishes the OAuth procedure by querying the Slack OAuth access url (`https://slack.com/api/oauth.access`). The resulting access_token is persistet in the AuthTokens table.
