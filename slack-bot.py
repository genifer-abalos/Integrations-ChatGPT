import openai
import slack
import os
from dotenv import load_dotenv
import ssl
import certifi
from datetime import date
import time

# add this line to point to your certificate path
ssl_context = ssl.create_default_context(cafile=certifi.where())
load_dotenv()

client = slack.WebClient(os.environ['SLACK_BOT_TOKEN'], ssl=ssl_context)

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

# client.chat_postMessage(channel="#chatgpt-convo", text="Hi!")
client.chat_postMessage(channel="#chatgpt-convo", text="The current date is " + str(date.today()) + " " + str(current_time))


