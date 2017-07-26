import json
import urllib
import base64

def create_send_slack_message(in_channel, location_for, change_url, image_url, created_by, created_on, token):
    return base64.urlsafe_b64encode(urllib.urlencode({
            "token": token,
            "channel": in_channel,
            "link_names": "true",
            "as_user": "false",
            "response_type": "in_channel",
            "attachments": json.dumps([{
                    "title": "Location of " + location_for + ", click <" + change_url + "|here> to update.",
                    "color": "#36a64f",
                    "image_url": image_url,
                    "attachment_type": "default",
                    "footer": "Location added by " + created_by + " <!date^" + created_on + "^ on {date} at {time}.|.>"
                    }])
            }))


def create_slack_response (in_channel, location_for, image_url, change_url, created_by, created_on, token):
    return json.dumps(
            {
                "attachments": [
                    {
			"title": "Location of " + location_for + ", click <" + change_url + "|here> to update.",
                        "color": "#36a64f",
                        "image_url": image_url,
                        "fallback": "Someone sent you a location via /map.",
                        "callback_id": "map",
                        "attachment_type": "default",
			"footer": "Location added by " + created_by + " <!date^" + created_on + "^ on {date} at {time}.|.>",
                        "actions": [
                            {
                                "name": "send8037123",
                                "text": "Send",
                                "type": "button",
                                "value": create_send_slack_message(in_channel, location_for, change_url, image_url, created_by, created_on, token),
                                "style": "primary"
                                },
                            {
                                "name": "cancel8037123",
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

def create_slack_auth_response (client_id, redirect_uri):
    url = "https://slack.com/oauth/authorize?"
    url += urllib.urlencode({
        "client_id": client_id,
        "scope": "chat:write:user",
        "redirect_uri" : redirect_uri,
        })
    return json.dumps(
            {
                "text": "Please authorize this app *<" + url + "|here>*!"
            }
        )

def create_failed_slack_response (message):
    return json.dumps(
            {
                "text": "Something went terribly wrong :explodyparrot:. Please contact @tflend.\n`" + message + "`"
            }
        )
