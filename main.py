import random

# 引入套件 flask
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
# 引入 linebot 異常處理
from linebot.exceptions import (
    InvalidSignatureError
)
# 引入 linebot 訊息元件
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, VideoSendMessage
)

user_command_dict = {}

# 當作報明牌隨機的股票 list
selective_stocks = ['2330 台積電', '2317 鴻海', '2308 台達電', '2454 聯發科']

# 範例股價資訊，同學可以自行更換成查詢股價的爬蟲資料或是即時股價查詢套件的資料
stock_price_dict = {
    '2330': 210,
    '2317': 90,
    '2308': 150,
    '2454': 300
}

app = Flask(__name__)

# LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN 類似聊天機器人的密碼，記得不要放到 repl.it 或是和他人分享
line_bot_api = LineBotApi('')
handler = WebhookHandler('')


# 此為 Webhook callback endpoint
@app.route("/callback", methods=['POST'])
def callback():
    # 取得網路請求的標頭 X-Line-Signature 內容，確認請求是從 LINE Server 送來的
    signature = request.headers['X-Line-Signature']

    # 將請求內容取出
    body = request.get_data(as_text=True)

    # handle webhook body（轉送給負責處理的 handler，ex. handle_message）
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# decorator 負責判斷 event 為 MessageEvent 實例，event.message 為 TextMessage 實例。所以此為處理 TextMessage 的 handler
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply_message = TextSendMessage(text='Waht can I do for you?')
    user_id = event.source.user_id
    
    # 根據使用者 ID 暫存指令
    user_command = user_command_dict.get(user_id)

    # 根據使用者輸入 event.message.text 條件判斷要回應哪一種訊息
    #if user_message == 'text' or 'TEXT':
        
    #    reply_message = TextSendMessage(text=event.message.text)
        
    if user_message == 'pic':
        reply_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/WhuIQql.jpg',
            preview_image_url='https://i.imgur.com/WhuIQql.jpg'
            )
    if user_message == '@pic':
        reply_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/J6a2biS.jpg',
            preview_image_url='https://i.imgur.com/J6a2biS.jpg'
            )
        
    elif user_message == 'sticker':
        reply_message = StickerSendMessage(
            package_id='2',
            sticker_id='161'
            )
        
    elif user_message == '@sticker':
        reply_message = StickerSendMessage(
            package_id='2',
            sticker_id='46'
            )
        
    elif user_message == 'movie':
        reply_message = VideoSendMessage(
            original_content_url='https://i.imgur.com/0thlogL.mp4',
            preview_image_url='https://i.imgur.com/0thlogLm.mp4'
            )   
            
    elif user_message == '@query_by_code' and user_command != '@query_by_code':
        reply_message = TextSendMessage(text='Enter the stock\'s code you want to query:')
        user_command_dict[user_id] = '@query_by_code'
        
    elif user_message == '@selective_stocks':
        #random.choice 方法會從參數 list 隨機取出一個元素
        random_stock = random.choice(selective_stocks)
        reply_message = TextSendMessage(text=f'Selective Stock：{random_stock}')
        user_command_dict[user_id] = None
        
    elif user_command == '@query_by_code':
        stock_price = stock_price_dict[user_message]
        if stock_price:
            reply_message = TextSendMessage(text=f'Closing Price：{stock_price}')
            # 清除指令暫存
            user_command_dict[user_id] = None
            
    line_bot_api.reply_message(
        event.reply_token,
        reply_message)
    
# __name__ 為內建變數，若程式不是被當作模組引入則為 __main__
if __name__ == "__main__":
    # 運行 Flask server，設定監聽 port 8080（網路 IP 位置搭配 Port 可以辨識出要把網路請求送到那邊 xxx.xxx.xxx.xxx:port，0.0.0.0 代表任何 IP）
    app.run(host='0.0.0.0', port=8080)
