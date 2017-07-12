import json

def create_slack_response (location_for, image_url):
    return json.dumps(
            {
                "attachments": [
                    {
                        "title": "Change location in browser",
                        "title_link": image_url,
                        "text": "Location for " + location_for,
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

