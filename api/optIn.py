
import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def genOptInBlock(user):
        return [
            {
                        "type": "section",
                        "text": {
                                "type": "mrkdwn",
                                "text": "Hello @{name}!\n Would you like to Opt into next week's Coffee Roulette?".format(name = user['name'])
                        }
                },
                {
                        "type": "actions",
                        "elements": [
                                {
                                        "type": "button",
                                        "text": {
                                                "type": "plain_text",
                                                "text": "Yes!",
                                                "emoji": True
                                        },
                                        "url": "https://google.com"
                                },
                                {
                                        "type": "button",
                                        "text": {
                                                "type": "plain_text",
                                                "text": "No...",
                                                "emoji": True
                                        }
                                }
                        ]
                }
        ]

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

def sendOptIn(client, logger):
    try:
        result = client.users_list()
        users_array = result["members"]
        for user in users_array:
            if (user["id"] == "U03Q4H2MNCT"):
            # if (True):
                sendOptInHelper(client, logger, user)
    except SlackApiError as e:
        logger.error("Error creating conversation: {}".format(e))

if __name__ == '__main__':
    client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
    logger = logging.getLogger(__name__)
    sendOptIn(client, logger)

