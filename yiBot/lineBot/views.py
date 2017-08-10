from django.http.response import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from linebot.api import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models.events import MessageEvent
from linebot.models.messages import TextMessage
from linebot.models.send_messages import TextSendMessage
from linebot.webhook import WebhookParser

from yiBot.settings import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from lineBot.weatherApi import weatherApi

try:
    # 在local端沒有line的各項資料（channel access token & secret key），故本機端運行會直接卡死在這裡
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    parser = WebhookParser(LINE_CHANNEL_SECRET)    # 攔截傳到LINE帳號的訊息
except:
    line_bot_api = None
    parser = None

@csrf_exempt
def lineBot(request):
    if request.method == 'GET':
#         return weatherApi('text')
        return HttpResponse()
    
    # POST
    signature = request.META['HTTP_X_LINE_SIGNATURE']   # 取得簽章
    body = request.body.decode('utf-8')
    try:
        events = parser.parse(body, signature)    # 驗證簽章是否正確（是不是從LINE傳過來的）
    except InvalidSignatureError:    # 訊息並非來自 Line Server
        return HttpResponseForbidden()
    except LineBotApiError:    # Line Server問題
        return HttpResponseBadRequest()
     
    for event in events:
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage): # 確保為文字訊息                
                response = event.message.text
                if '@yibot' in response:
                    response.replace('@yibot', '')
                else:
                    continue
                print(response)
                
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=response)
                )
                
    return HttpResponse()
    
    
    