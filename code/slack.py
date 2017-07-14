import json
import urllib
import base64

def create_send_slack_message(in_channel, location_for, change_url, image_url, created_by, created_on):
    return base64.b32encode(urllib.urlencode({
            "token": 'xoxp-113070057776-211135045057-212852625397-a02dc2cae27533deca6f9583815fe60f',
            "channel": in_channel,
            "link_names": "true",
            "as_user": "true",
            "attachments": json.dumps([
                {
                    "title": "Location of " + location_for + ", click <" + change_url + "|here> to update.",
                    "color": "#36a64f",
                    "image_url": image_url,
                    "attachment_type": "default",
                    "footer": "Location added by " + created_by + " <!date^" + created_on + "^ on {date} at {time}.|.>"
                    }
                ])
            }))


def create_slack_response (in_channel, location_for, image_url, change_url, created_by, created_on):
    return json.dumps(
            {
                "attachments": [
                    {
			"title": "Location of " + location_for + ", click <" + change_url + "|here> to update.",
                        "color": "#36a64f",
                        "image_url": image_url,
                        "fallback": "Looks like your slack client is to old.",
                        "callback_id": "map",
                        "attachment_type": "default",
			"footer": "Location added by " + created_by + " <!date^" + created_on + "^ on {date} at {time}.|.>",
                        "actions": [
                            {
                                "name": "send",
                                "text": "Send",
                                "type": "button",
                                "value": create_send_slack_message(in_channel, location_for, change_url, image_url, created_by, created_on),
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
