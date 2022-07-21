from app.models.profile import Profile

def created_profile_home(profile : Profile):
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Profile",
                    "emoji": True
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Name*\n{profile.name}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Status*\n{'Intern' if profile.is_intern else 'Full-time Employee'}"
                }
            },
            {
                "type": "section",
                "block_id": "edit_profile",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Preference*\n{'Interns and Full-time Employees' if len(profile.prefers) == 2 else profile.prefers[0]}"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Edit Profile",
                        "emoji": True
                    },
                    # "value": "click_me_123",
                    "value": "opt-in/Yes",
                    "action_id": "button-action"
                }
            }
        ]
    }

UNCREATED_PROFILE_HOME = {
	"blocks": [
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Create Profile",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "actionId-0"
				}
			]
		}
	]
}