import json
import os
import requests
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import ApiClient, MessagingApi, Configuration, ReplyMessageRequest, TextMessage
from response_message import get_definition

# get Token from AWS Environment Variables
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

configuration = Configuration(access_token=ACCESS_TOKEN)

def lambda_handler(event, context):
    body = json.loads(event["body"])
    
    # check message from LINE
    if "events" in body:
        for e in body["events"]:
            if e["type"] == "message" and "text" in e["message"]:
                reply_token = e["replyToken"]
                text = e["message"]["text"]
                
                # reply message to LINE
                with ApiClient(configuration) as api_client:
                    line_bot_api = MessagingApi(api_client)
                    
                    reply_message = get_definition(text)

                    line_bot_api.reply_message(
                        ReplyMessageRequest(
                            reply_token=reply_token,
                            messages=[reply_message]
                        )
                    )
    
    return {"statusCode": 200, "body": "OK"}
