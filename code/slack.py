import json

def create_slack_response (location_for, image_url, change_url, created_by, created_on):
    return json.dumps(
            {
                "attachments": [
                    {
			"title": "Location of " + location_for + ", click <" + change_url + "|here> to update.",
                        "color": "#36a64f",
                        "image_url": image_url,
                        "attachment_type": "default",
			"footer": "Location added by " + created_by + ".",
                        "ts": created_on,
                        "actions": [
                            {
                                "name": "send",
                                "text": "Send",
                                "type": "button",
                                "value": "send",
                                "style": "primary"
                                },
                            {
                                "name": "cancel",
                                "text": "Cancel",
                                "type": "button",
                                "value": "cancel"
                                }
                            ]
                        }
                    ]
                }
            )

def create_slack_response_not_found (location_for, change_url):
    return json.dumps(
            {
                "text": "Whoops, it looks like we don't know where *" + location_for + "* is :sadparrot:.\n" 
                + "Please help us out by setting the location *<" + change_url + "|here>*!"
            }
        )

def create_failed_slack_response (message):
    return json.dumps(
            {
                "text": "Something went terribly wrong :explodyparrot:. Please contact @tflend.\n`" + message + "`"
            }
        )
