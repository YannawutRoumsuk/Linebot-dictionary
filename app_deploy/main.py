import os
import json
from fastapi import FastAPI, Request, HTTPException, Header
from mangum import Mangum  # ใช้ Mangum แปลง FastAPI เป็น Lambda Handler เพื่อ Deploy ขึ้น aws lambda

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from linebot.v3.messaging import (
    ApiClient, 
    MessagingApi, 
    Configuration, 
    ReplyMessageRequest, 
    TextMessage
)
from response_message import get_definition  # ฟังก์ชันตอบกลับ LINE

app = FastAPI()
# ใช้ Mangum เพื่อให้ FastAPI ทำงานบน AWS Lambda
handler = Mangum(app)

# ดึงค่า Token จาก AWS Environment Variables
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

configuration = Configuration(access_token=ACCESS_TOKEN)
handler = WebhookHandler(channel_secret=CHANNEL_SECRET)

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    
    body = await request.body()
    body_str = body.decode('utf-8')
    
    try:
        handler.handle(body_str, x_line_signature)
        
    except InvalidSignatureError:
        
        print("Invalid signature. Please check your channel access token/channel secret.")
        raise HTTPException(status_code=400, detail="Invalid signature.")

    return {"status": "OK"}

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        word = event.message.text
        reply_message = get_definition(word)

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[reply_message]
            )
        )


