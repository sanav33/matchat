# TO BE RENAMED TO send_opt_in.py
import logging
import os
from flask import request, Blueprint, Response
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from app.block_kits.opt_in_block import genOptInBlock
from slack_sdk.errors import SlackApiError


def sendOptInHelper(client, logger, user):
    try:
    # Call the chat.postMessage method using the WebClient
        result = client.chat_postMessage(
            channel=user['id'],
            text=":)",
            blocks=genOptInBlock(user)
        )
        logger.info(result)

    except SlackApiError as e:
        logger.error(f"Error posting message: {e}") 

send_opt_in = Blueprint('send_opt_in', __name__)
@send_opt_in.post('/send_opt_in')
def sendOptIn():
    try:
        client, logger = WebClient(token=os.environ.get("SLACK_BOT_TOKEN")), logging.getLogger(__name__)
        users_array = client.users_list()["members"]
        for user in users_array:
                sendOptInHelper(client, logger, user)
        return Response(status=200)
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))
        return Response(status=400) 

