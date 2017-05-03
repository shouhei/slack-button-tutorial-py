from flask import Flask, request
import os
import requests
import json

APP_VERIFICATION_TOKEN = os.getenv('APP_VERIFICATION_TOKEN', "")

app = Flask(__name__)


@app.route('/slack/actions', methods=['POST'])
def actions():
    action_json_payload = json.loads(request.form['payload'])
    text = action_json_payload['user']['name'] \
        + " clicked: " \
        + action_json_payload['actions'][0]['name']
    message = {
        "text": text,
        "replace_original": False
    }
    requests.post(action_json_payload['response_url'], json=message)
    return "actions"


@app.route('/slack/slash-commands/send-me-buttons', methods=['POST'])
def send_me_buttons():
    if (request.form['token'] != APP_VERIFICATION_TOKEN):
            return "", 403
    message = {
        "text": "This is your first interactive message",
        "attachments": [
            {
                "text": "Building buttons is easy right?",
                "fallback": "Shame... buttons aren't supported in this land",
                "callback_id": "button_tutorial",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "yes",
                        "text": "yes",
                        "type": "button",
                        "value": "yes"
                    },
                    {
                        "name": "no",
                        "text": "no",
                        "type": "button",
                        "value": "no"
                    },
                    {
                        "name": "maybe",
                        "text": "maybe",
                        "type": "button",
                        "value": "maybe",
                        "style": "danger"
                    }
                ]
            }
        ]
    }
    requests.post(request.form['response_url'], json=message)
    return "send-me-buttons"


if __name__ == "__main__":
    app.run(debug=True)
