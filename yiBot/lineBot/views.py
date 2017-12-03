from django.http.response import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import linebot
from linebot.api import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models.events import MessageEvent
from linebot.models.imagemap import ImagemapSendMessage, BaseSize, \
    URIImagemapAction, ImagemapArea, MessageImagemapAction
from linebot.models.messages import TextMessage
from linebot.models.send_messages import TextSendMessage, ImageSendMessage, StickerSendMessage
from linebot.models.template import ConfirmTemplate, MessageTemplateAction, \
    TemplateSendMessage, ButtonsTemplate, URITemplateAction, \
    PostbackTemplateAction, CarouselTemplate, CarouselColumn, \
    ImageCarouselTemplate, ImageCarouselColumn, DatetimePickerTemplateAction
from linebot.webhook import WebhookParser

from lineBot.drawCard import drawCard
from lineBot.meme import findMeme
from lineBot.models import LineUser
from lineBot.weatherApi import weatherApi
from yiBot.settings import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET


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
        replyID = updateUserList(event)
        
        if isinstance(event, MessageEvent):
            if isinstance(event.message, TextMessage): # 確保為文字訊息                
                msg = event.message.text
                if '@yibot' in msg:
                    msg = msg.replace('@yibot', '').strip()
                elif '@imgmap' in msg:                    
                    # FIXME: 沒作用
                    imagemap_message = ImagemapSendMessage(
                        base_url='https://example.com/base',
                        alt_text='this is an imagemap',
                        base_size=BaseSize(height=1040, width=1040),
                        actions=[
                            URIImagemapAction(
                                link_uri='https://example.com/',
                                area=ImagemapArea(
                                    x=0, y=0, width=520, height=1040
                                )
                            ),
                            MessageImagemapAction(
                                text='hello',
                                area=ImagemapArea(
                                    x=520, y=0, width=520, height=1040
                                )
                            )
                        ]
                    )                    
                    line_bot_api.reply_message(event.reply_token, imagemap_message)
                    continue
                elif '@confirm' in msg:
                    confirm_template = ConfirmTemplate(text='Do it?', actions=[
                        MessageTemplateAction(label='Yes', text='Yes!'),
                        MessageTemplateAction(label='No', text='No!'),
                    ])
                    template_message = TemplateSendMessage(
                        alt_text='Confirm alt text', template=confirm_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                    continue
                
                elif '@button' in msg:
                    buttons_template = ButtonsTemplate(
                        title='My buttons sample', text='Hello, my buttons', actions=[
                            URITemplateAction(
                                label='Go to line.me', uri='https://line.me'),
                            PostbackTemplateAction(label='ping', data='ping'),
                            PostbackTemplateAction(
                                label='ping with text', data='ping',
                                text='ping'),
                            MessageTemplateAction(label='Translate Rice', text='米')
                        ])
                    template_message = TemplateSendMessage(
                        alt_text='Buttons alt text', template=buttons_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                    continue
                
                elif '@carousel' in msg:
                    carousel_template = CarouselTemplate(columns=[
                        CarouselColumn(text='hoge1', title='fuga1', actions=[
                            URITemplateAction(
                                label='Go to line.me', uri='https://line.me'),
                            PostbackTemplateAction(label='ping', data='ping')
                        ]),
                        CarouselColumn(text='hoge2', title='fuga2', actions=[
                            PostbackTemplateAction(
                                label='ping with text', data='ping',
                                text='ping'),
                            MessageTemplateAction(label='Translate Rice', text='米')
                        ]),
                    ])
                    template_message = TemplateSendMessage(
                        alt_text='Carousel alt text', template=carousel_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                    continue
                elif '@img_carousel' in msg:
                    image_carousel_template = ImageCarouselTemplate(columns=[
                        ImageCarouselColumn(image_url='https://dvblobcdnea.azureedge.net//Content/Upload/Popular/Images/2017-06/e99e6b5e-ca6c-4c19-87b7-dfd63db6381a_m.jpg',
                                            action=DatetimePickerTemplateAction(label='datetime',
                                                                                data='datetime_postback',
                                                                                mode='datetime')),
                        ImageCarouselColumn(image_url='https://cdn2.ettoday.net/images/2457/d2457712.jpg',
                                            action=DatetimePickerTemplateAction(label='date',
                                                                                data='date_postback',
                                                                                mode='date'))
                    ])
                    template_message = TemplateSendMessage(
                        alt_text='ImageCarousel alt text', template=image_carousel_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                
                
                
                
                
                elif '@send' in msg:
                    if not isCommander(event.source.user_id):
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='歹勢，您無權限'))
                        continue
                    msg = msg.replace('@send', '').split(', ')
                    to, message = msg[0], msg[1]
                    line_bot_api.push_message(to, TextMessage(text=message))
                    continue
                elif '@抽卡' in msg:
                    msg = msg.replace('@抽卡', '')
                    result = drawCard(msg)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
                    continue
                elif '@天氣' in msg:
                    msg = msg.replace('@天氣', '').replace('台', '臺').strip()
                    success, response = weatherApi(msg)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
                    if not success:
                        line_bot_api.push_message(replyID, StickerSendMessage(package_id='2', sticker_id='38'))
                    continue
                else:
                    continue
                
                imgURL = findMeme(msg)
                if not imgURL:
#                     line_bot_api.reply_message(
#                         event.reply_token,
#                         TextSendMessage(text=response)
#                     )
                    #FIXME: 只能reply一次，想辦法把用戶ID記住，再傳一次
                    line_bot_api.reply_message(
                        event.reply_token,
                        StickerSendMessage(package_id='2',
                                           sticker_id='38')
                    )
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
                print(msg, imgURL)
                
    return HttpResponse()
    
    
def updateUserList(event):
    #===========================================================================
    # 檢查userID/groupID/roomID是否已存在，若否則新增該筆資訊
    #===========================================================================
    source = event.source
    userID = source.user_id
    chatType = source.type
    
    if chatType == 'group':
        replyID = source.group_id
#         profile = line_bot_api.get_group_member_profile(replyID, userID)
        LineUser.objects.get_or_create(chatFrom='group', lineID=replyID)
    elif chatType == 'room':
        replyID = source.room_id
#         profile = line_bot_api.get_room_member_profile(replyID, userID)
        LineUser.objects.get_or_create(chatFrom='room', lineID=replyID)
    else:    #user
        replyID = userID
        profile = line_bot_api.get_profile(userID)
        user = LineUser.objects.filter(lineID=userID)
        if not user:
            LineUser.objects.create(name=profile.display_name, chatFrom='user', lineID=userID)
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
    
    return replyID

    
def isCommander(userID):
    user = get_object_or_404(LineUser, lineID=userID)
    if user.commander:
        return True
    
    return False
    
    
    
