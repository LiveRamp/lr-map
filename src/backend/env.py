import os
import sys

if "PROD" in os.environ:
    link_to_frontend = "http://***REMOVED***.s3-website-us-east-1.amazonaws.com/"
    link_to_db_helper = 'https://***REMOVED***.execute-api.us-east-1.amazonaws.com/prod/***REMOVED***-db-helper'
    url = "https://slack.com/oauth/authorize?client_id=***REMOVED***&scope=chat%3Awrite%3Auser&redirect_uri=https%3A%2F%2F***REMOVED***.execute-api.us-east-1.amazonaws.com%2Fprod%2F***REMOVED***-db-helper-staging"
    bucket = "slack-map-images"
    LOCATIONS_TABLE_NAME = "MapLocations"
    AUTH_TABLE_NAME = "AuthTokens"
    slack_client_id = "***REMOVED***"
    slack_client_secret = "***REMOVED***"
elif "TEST" in os.environ:
    link_to_frontend = "http://***REMOVED***-staging.s3-website-us-east-1.amazonaws.com/"
    link_to_db_helper = 'https://***REMOVED***.execute-api.us-east-1.amazonaws.com/prod/***REMOVED***-db-helper-staging'
    bucket = "***REMOVED***"
    LOCATIONS_TABLE_NAME = "MapLocationsStaging"
    AUTH_TABLE_NAME = "AuthTokensStaging"
    slack_client_id = "***REMOVED***"
    slack_client_secret = "***REMOVED***"
else:
    sys.exit(1)
