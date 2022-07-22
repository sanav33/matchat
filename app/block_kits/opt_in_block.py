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
                                                "text": "Yes",
                                                "emoji": True
                                        },
                                        "value": "Yes",
                                },
                                {
                                        "type": "button",
                                        "text": {
                                                "type": "plain_text",
                                                "text": "No",
                                                "emoji": True
                                        },
                                        "value": "Yes",
                                }
                        ]
                }
        ]