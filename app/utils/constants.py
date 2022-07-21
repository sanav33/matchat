from os import environ

SLACK_API_URL = environ.get("SLACK_API_URL")
ATLAS_CONNECTION_STR = environ.get("ATLAS_CONNECTION_STR")
SLACK_USER_ID = environ.get("SLACK_USER_ID")

API_VIEWS_PUBLISH = "/api/views.publish"