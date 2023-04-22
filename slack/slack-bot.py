import json
import openai
import slack
from slack import WebhookClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
import ssl
import certifi
from datetime import date
import time

from flask import Flask, request, make_response
app = Flask(__name__)

load_dotenv()

from slack_sdk.signature import SignatureVerifier
signature_verifier = SignatureVerifier(
    signing_secret=os.environ['SLACK_SIGNING_SECRET']
)


# add this line to point to your certificate path
ssl_context = ssl.create_default_context(cafile=certifi.where())
ssl_context2 = ssl.create_default_context()
ssl_context2.check_hostname = False
ssl_context2.verify_mode = ssl.CERT_NONE


client = slack.WebClient(os.environ['SLACK_BOT_TOKEN'], ssl=ssl_context2)
openai.api_key = os.environ['CHATGPT_API_KEY']


t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
client.chat_postMessage(channel="#chatgpt-convo", text="Python app initiated for Slack Bot at "
                       "" + str(date.today()) + " " + str(current_time) + ". " +
                       "Start your message with @ChatGPT then type your message/question")


def get_chatgpt_response(the_prompt, thread_ts):
    chatgpt_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=the_prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5).choices[0].text

    print(chatgpt_response)

    # Reply as a new message
    # response = client.chat_postMessage(channel="#chatgpt-convo", text=f"Here you go: \n{response}")

    # This is used if you needto specify the channel url webhook instead of the channel name
    # webhook = WebhookClient(os.environ['CHANNEL_URL_CHATGPT_CONVO'], ssl=ssl_context)

    # Reply to the message/event thread
    response = client.chat_postMessage(
        channel="#chatgpt-convo",
        text=chatgpt_response,
        # thread_ts="1561764011.015500"
        thread_ts=thread_ts,
    )

    print(response.status_code)


def create_ticket_from_mentions():
    pass
    # Idea: If the user mentions @Tech, we will create a ticket for them
    # Reply with a section and link
    # response = webhook.send(
    #     text="fallback",
    #     blocks=[
    #         {
    #             "type": "section",
    #             "text": {
    #                 "type": "mrkdwn",
    #                 "text": "You have a new request:\n*<link.com>|Genifer Abalos - New ticket request>*"
    #             }
    #         }
    #     ]
    # )


@app.route("/", methods=["GET", "POST"])
def home():
    print(f"Connecting webhooks")
    request_body = request.data
    print(f"{request_body = }")

    return request_body


@app.route("/slack/events", methods=["POST"])
def slack_app():
    # Verify incoming requests from Slack @mentions
    print(f"Connecting /slack/events")
    request_body = request.data
    print(f"{request_body = }")

    prompt = json.loads(request_body)['event']['text']
    thread_ts = json.loads(request_body)["event"]["ts"]
    get_chatgpt_response(the_prompt=prompt, thread_ts=thread_ts)

    return request_body


if __name__ == '__main__':
    # Get event from Slack
    # Get the prompt from Slack mentions
    # Pass it to ChatGPT API
    # Fetch ChatGPT response
    # Post response to slack channel and thread

    app.run(debug=True, port=8081)

