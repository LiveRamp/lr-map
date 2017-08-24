# slack map
This project lets you use **/map** in Slack to find and share the location of meeting rooms, people or anything else.

## Technical Overview
The app heavily uses different [AWS](https://aws.amazon.com/) services, namely: [Lambda](https://aws.amazon.com/lambda/), [DynamoDB](https://aws.amazon.com/dynamodb/) and [S3](https://aws.amazon.com/s3/).

The production app is replicated in a staging environment in order to make it possible to test new changes without disturbing current users. In this readme, everything will be described in terms of production, however staging is identical except the services have the suffix **-staging**. 

There are two lambdas being used: the *app lambda* takes care of all the slack interactions. The *db lambda* is used for database entry. They are located at [src/backend/main_app.py] and [src/backend/main_db.py].

The static content is stored in two buckets on S3. The *static content bucket* is used for hosting the website and the *image bucket* is used to store and serve the resulting gifs.

There are two tables in DynamoDB. The *MapLocations table* contains all the location data and the *AuthTokens table* contains the access tokens which enable the app to send messages on behalf of the user.

## Technical Details
The **/map** callback URL is set in the *Slash commands* section of the Slack App. This URL is queried whenever a user types **/map**. When a user presses a button on a message returned by the app the interactive messages URL is being called. This URL is set in the *Interactive messages* section. Both URLs should point to the main_app.py lambda.

## Setting it up
To set up the slack map, one has to create two S3 buckets, two AWS Lambdas and two DynamoDB tables. The credentials should be stored in src/backend/env.py.

The first bucket hosts static content of the website. The second bucket hosts images that are generated and later fetched by Slack. The first lambda executes ./src/backend/main_db.py, is responsible for storing authorization info and location info into the DynamoDB, and is called by the websites. The second lambda executes ./src/main_app.py, fetches the location data from the DB, and is called by using the Slack command.

The lambdas should have an environmental variable set, either "PROD" or "TEST", depending on whether it's the production or testing environment. For safety reasons, if none of them is set, the lambda will exit with an error.

### Getting the access_token
The first step every user has to complete is to give the app the rights to send messages as the user. This is important since we can not post to direct message channels otherwise. Please refer to the [Slack documentation](https://api.slack.com/docs/oauth) for how the authentication works.

The first request the user sends is processed by main_app.py. It checks if the AuthTokens table contains an access_token for this user's id. If this is not the case a Slack message is returned which contains a link to the slack authentication URL (`https://slack.com/oauth/authorize?`) with all the necessary parameters. After the user clicks the Authorize button he is redirected to the URL specified in the *OAuth & Permissions* section of the Slack app. This URL points to the main_db lambda which finishes the OAuth procedure by querying the Slack OAuth access URL (`https://slack.com/api/oauth.access`). The resulting access_token is persisted in the AuthTokens table.

### Returning a location
To return a location, the main_app.py gets the location from the MapLocations table, generates the gif and returns the message in the HTTP response-body. One thing to note is that all the information that is used when the user clicks **Send** on the resulting message is already encoded in the send button.

### Sharing a location
When the user clicks **Send**, main_app.py gets called again and returns the instruction to delete the current message (the one with the send and cancel button). At the same time, the Slack's postMessage URL (`https://slack.com/api/chat.postMessage`) is queried to post the message publicly. This is done because the message type can not be changed from private to public. So we need to delete the private message and post a public one using the information encoded in the send button. This information especially includes the user's acces_token.

### Setting a location
If the location cannot be found in the database, the main_app.py returns a message containing the link to the static website hosted in the static content bucket of S3. This link has some information encoded in it that the db lambda needs for the database entry as well as some information for the frontend. When the user persists a location main_db.py is called and the location is persisted in the MapLocations table.

### Encoding
The information that is encoded in the buttons or the frontend URL is encoded using Python's [base64.urlsafe_b64encode](https://docs.python.org/2/library/base64.html) method. This prevents the data from being escaped by Slack.
