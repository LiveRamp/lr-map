import os
import sys

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
