import json

def create_slack_response (location_for, image_url, location):
    return json.dumps(
            {
                "attachments": [
                    {
                        "title": "Change location in browser",
                        "title_link": image_url,
                        "text": "Location of " + location + " for user " + location_for,
                        "color": "#36a64f",
                        "image_url": image_url,
                        "attachment_type": "default",
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


def create_failed_slack_response(message):
    return json.dumps(
        {
                "attachments": [
                    {
                        "title": "An error has occurred",
                        "text": message,
                        "color": "#36a64f",
                        "attachment_type": "default",
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