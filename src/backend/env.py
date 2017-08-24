import os
import sys
# Please complete the credentials for both production and staging environment.
#
# link_to_frontend is the link to the static content on s3.
# link_to_db_helper is the link to the lambda that has the db helper.
# bucket is the name of the S3 bucket with pictures.
# LOCATIONS_TABLE_NAME is the name of the DynamoDB table storing locations.
# AUTH_TABLE_NAME is the name of the DynamoDB table storing authorization information.
# slack_client_id is the client ID copied from Slack's App Credentials.
# slack_client_secret is the client Secret copied from Slack's App Credentials.
# team_id is the ID of your slack team.

if "PROD" in os.environ:
    link_to_frontend =
    link_to_db_helper =
    bucket =
    LOCATIONS_TABLE_NAME =
    AUTH_TABLE_NAME =
    slack_client_id =
    slack_client_secret =
    team_id =
elif "TEST" in os.environ:
    link_to_frontend =
    link_to_db_helper =
    bucket =
    LOCATIONS_TABLE_NAME =
    AUTH_TABLE_NAME =
    slack_client_id =
    slack_client_secret =
    team_id =
else:
    sys.exit(1)
