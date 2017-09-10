from django.http.response import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import linebot
from linebot.api import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models.events import MessageEvent
from linebot.models.messages import TextMessage
from linebot.models.send_messages import TextSendMessage, ImageSendMessage, StickerSendMessage
from linebot.webhook import WebhookParser

from yiBot.settings import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET
from lineBot.weatherApi import weatherApi
from lineBot.meme import findMeme
from lineBot.models import LineUser
from django.shortcuts import get_object_or_404

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
        updateUserList(event)
        
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage): # 確保為文字訊息                
                response = event.message.text
                if '@yibot' in response:
                    response = response.replace('@yibot', '').strip()
                elif '@send' in response and isCommander(event.source.user_id):
                    response = response.replace('@send', '').split(', ')
                    to, message = response[0], response[1]
                    line_bot_api.push_message(to, TextMessage(text=message))
                    continue
                else:
                    continue
                
                imgURL = findMeme(response)
                if not imgURL:
                    try:
#                         line_bot_api.reply_message(
#                             event.reply_token,
#                             TextSendMessage(text=response)
#                         )
                        #FIXME: 只能reply一次，想辦法把用戶ID記住，再傳一次
                        line_bot_api.reply_message(
                            event.reply_token,
                            StickerSendMessage(package_id='2',
                                               sticker_id='38')
                        )
                    except linebot.exceptions.LineBotApiError as e:
                        print('錯誤代碼:', e.status_code)
                        print('錯誤訊息:', e.error.message)
                        print('詳細資訊:', e.error.details)
                    continue
                
                try:
                    line_bot_api.reply_message(
                        event.reply_token,
                        ImageSendMessage(original_content_url=imgURL,
                                         preview_image_url=imgURL)
                    )
                except linebot.exceptions.LineBotApiError as e:
                    print('錯誤代碼:', e.status_code)
                    print('錯誤訊息:', e.error.message)
                    print('詳細資訊:', e.error.details)
                    print('可在 https://devdocs.line.me/en/#common-specifications 查到對應代碼及錯誤')
                print(response, imgURL)
                
    return HttpResponse()
    
    
def updateUserList(event):
    #===========================================================================
    # 檢查userID/groupID/roomID是否已存在，若否則新增該筆資訊
    #===========================================================================
    source = event.source
    userID = source.user_id
    chatType = source.type
    print(source, userID, chatType)
    profile = line_bot_api.get_profile(userID)
#     print(profile.display_name)    #使用者姓名
#     print(profile.user_id)    #使用者ID
#     print(profile.picture_url)    #使用者大頭照網址
#     print(profile.status_message)    #使用者簽名檔
    
#     try:
#         LineUser.objects.get(lineID=userID)
#     except ObjectDoesNotExist:
#         LineUser.objects.create(name=profile.display_name, type='user', lineID=userID)
    #寫了exception還是會爆炸，在ObjectDoesNotExist中print東西是正常運作的
    #但是程式就是會一直卡在get error那邊不明所以，故改採filter的方式
    
    user = LineUser.objects.filter(lineID=userID)
    if not user:
        LineUser.objects.create(name=profile.display_name, chatFrom='user', lineID=userID)
    
    if chatType == 'group':
        LineUser.objects.get_or_create(chatFrom='group', lineID=source.group_id)
    
    if chatType == 'room':
        LineUser.objects.get_or_create(chatFrom='room', lineID=source.room_id)
    
    
def isCommander(userID):
    user = get_object_or_404(LineUser, lineID=userID)
    if user.commander:
        return True
    
    return False
    
    
    
