# liveramp_map
This app lets you use **/map** in Slack to find and share the location of meeting rooms, people or anything else.

## Technical Overview
The app heavily uses the different [AWS](https://aws.amazon.com/) services, namely: [Lambda](https://aws.amazon.com/lambda/), [S3](https://aws.amazon.com/s3/) and [DynamoDB](https://aws.amazon.com/dynamodb/). Everything is replicated in a staging environment to enable testing via the [AcxiomSandbox](acxiom-sandbox.slack.com) Slack team.

In the following everything will be described in terms of production, staging is identical except the services have **-staging** appended.

There are two lambdas the [app lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/***REMOVED***?tab=code) takes care of all the slack interactions. The [db lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions/***REMOVED***-db-helper?tab=code) is used for database entry. They are located at [src/backend/main_app.py](https://git.liveramp.net/MasterRepos/liveramp_map/blob/master/src/backend/main_app.py) and [src/backend/main_db.py](https://git.liveramp.net/MasterRepos/liveramp_map/blob/master/src/backend/main_db.py).

The static content ist stored in two buckets on S3. The [static content bucket](https://s3.console.aws.amazon.com/s3/buckets/***REMOVED***/?region=us-east-1&tab=overview) is used for hosting the website and the [image bucket](https://s3.console.aws.amazon.com/s3/buckets/slack-map-images/?region=us-east-1&tab=overview) is used to store and serve the resulting gifs.

There are two tables in DynamoDB. The [MapLocations table](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=MapLocations) contains all the location data and the [AuthTokens table](https://console.aws.amazon.com/dynamodb/home?region=us-east-1#tables:selected=AuthTokens) contains the access tokens which enable the app to send messages on behalve of the user.
