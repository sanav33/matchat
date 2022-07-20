PROFILE_MODAL_DICT = {
	"type": "modal",
	"title": {
		"type": "plain_text",
		"text": "My App",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit",
		"emoji": True
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Edit Profile",
				"emoji": True
			}
		},
		{
			"type": "input",
            "block_id": "emp_type",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Full-timer",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Intern",
							"emoji": True
						},
						"value": "value-1"
					}
				],
				"action_id": "static_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Employee Type",
				"emoji": True
			}
		},
        {
			"type": "input",
			"block_id": "preference",
			"element": {
				"type": "multi_static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select options",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Interns",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Full-time Employees",
							"emoji": True
						},
						"value": "value-1"
					}
				],
				"action_id": "preference-multi_static_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Label",
				"emoji": True
			}
		}
    ]
}