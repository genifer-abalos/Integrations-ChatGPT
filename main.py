import openai
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_bolt import App
import ssl
import certifi
from flask import Flask, request, make_response
app = Flask(__name__)

from slack_sdk.signature import SignatureVerifier
signature_verifier = SignatureVerifier(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# add this line to point to your certificate path
ssl_context = ssl.create_default_context(cafile=certifi.where())


KEY = {
    "GPT_STEVE": "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"
}

SLACK_API_TOKEN_GENIFER = 'xapp-1-A0545PAN8MB-5147233887652-5443e604233145869c7da8c92751fd11c673a03c9cf5e5562afa2844fa04bce0'
SLACK_BOT_TOKEN_GENIFER = 'xoxb-5141768566597-5144776465490-kIbe4uVkPRzmQOuwjf59bwMi'


openai.api_key = KEY["GPT_STEVE"]
# Event API & Web API
app = App(token=SLACK_BOT_TOKEN_GENIFER)
client = WebClient(SLACK_BOT_TOKEN_GENIFER, ssl=ssl_context)


# This gets activated when the bot is tagged in a channel
@app.event("app_mention")
def handle_message_events(body, logger):
    # Log message
    print(str(body["event"]["text"]).split(">")[1])

    # Create prompt for ChatGPT
    prompt = str(body["event"]["text"]).split(">")[1]

    # Let thre user know that we are busy with the request
    response = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Hello from your bot! :robot_face: \nThanks for your request, I'm on it!")

    # Check ChatGPT
    openai.api_key = KEY["GPT_STEVE"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5).choices[0].text

    # Reply to thread
    response = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Here you go: \n{response}")


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_API_TOKEN_GENIFER).start()
    # flask_app.run(Debug=True)

# prompt = "Is linkedin learning premium worth it?"
# print(f"Genifer (App): {prompt}")
#
# # Generate a response from ChatGPT
# response = openai.Completion.create(
#     engine="text-davinci-003",
#     prompt=prompt,
#     max_tokens=1024,
#     temperature=0.5,
# )
# print(response)
# # Print the response
# print(f"GPT: {response['choices'][0]['text']}")
