from django.http.response import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import linebot
from linebot.api import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models.events import MessageEvent
from linebot.models.messages import TextMessage
from linebot.models.send_messages import TextSendMessage, ImageSendMessage
from linebot.webhook import WebhookParser

from yiBot.settings import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from lineBot.weatherApi import weatherApi
from lineBot.meme import findMeme

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
                    response = response.replace('@yibot', '').strip()
                else:
                    continue
                print(response)
                
                imgURL = findMeme(response)
                try:
                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(original_content_url=imgURL,
                                         preview_image_url=imgURL)
                    )
                except linebot.exceptions.LineBotApiError as e:
                    print('圖片網址:', imgURL)
                    print('錯誤代碼:', e.status_code)
                    print('錯誤訊息:', e.error.message)
                    print('詳細資訊:', e.error.details)
                    print('可在 https://devdocs.line.me/en/#common-specifications 查到對應代碼及錯誤')
                    
                '''
                try:
                    imgURL = findMeme(response)
                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(original_content_url=imgURL,
                                         preview_image_url=imgURL)
                    )
                except:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=response)
                    )
                '''
    return HttpResponse()
    
    
    
