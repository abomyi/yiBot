from django.http.response import HttpResponse, HttpResponseForbidden, \
    HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import linebot
from linebot.api import LineBotApi
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models.actions import PostbackAction, MessageAction, URIAction
from linebot.models.events import MessageEvent
from linebot.models.flex_message import FlexSendMessage
from linebot.models.imagemap import ImagemapSendMessage, BaseSize, \
    URIImagemapAction, ImagemapArea, MessageImagemapAction
from linebot.models.messages import TextMessage
from linebot.models.send_messages import TextSendMessage, ImageSendMessage, StickerSendMessage
from linebot.models.template import ConfirmTemplate, TemplateSendMessage, ButtonsTemplate, \
    CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn
from linebot.webhook import WebhookParser

from lineBot.drawCard import drawCard
from lineBot.meme import findMeme
from lineBot.models import LineUser
from lineBot.weatherApi import weatherApi
from main.constant import IMG_1, IMG_2
from todoList.views import todoList
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
                
                if msg.startswith('@yibot') or msg.startswith('@圖 '):
                    if msg.startswith('@yibot'):
                        msg = msg.replace('@yibot', '').strip()
                    else:
                        msg = msg[3:]
                    
                    
                elif '@list' in msg:
                    response = todoList(replyID, 'show')
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
                    continue
                elif '@todo' in msg:
                    msg = msg.replace('@todo', '').strip()
                    response = todoList(replyID, 'createItem', msg)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
                    continue
                elif '@done' in msg:
                    msg = msg.replace('@done', '').strip()
                    response = todoList(replyID, 'doneItem', msg)
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
                    continue
                elif '@clear' in msg:
                    response = todoList(replyID, 'clearItem')
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
                    continue
                                
                
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
                        PostbackAction(
                            label='postback',
                            display_text='postback text',
                            data='action=buy&itemid=1'
                        ),
                        MessageAction(
                            label='message',
                            text='message text'
                        )
                    ])
                    template_message = TemplateSendMessage(
                        alt_text='Confirm alt text', template=confirm_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                    continue
                
                elif '@button' in msg:
                    # 最多4個按鈕，超過會raise error
                    buttons_template = ButtonsTemplate(
                        title='My buttons sample', text='Hello, my buttons', actions=[
                            PostbackAction(
                                label='postback',
                                display_text='postback text',
                                data='action=buy&itemid=1'
                            ),
                            MessageAction(
                                label='message',
                                text='message text'
                            ),
                            URIAction(
                                label='uri',
                                uri='http://example.com/'
                            )
                        ])
                    template_message = TemplateSendMessage(
                        alt_text='Buttons alt text', template=buttons_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                    continue
                
                elif '@carousel' in msg:
                    carousel_template = CarouselTemplate(columns=[
                        CarouselColumn(title='this is menu1', text='description1', actions=[
                            PostbackAction(
                                label='postback1',
                                display_text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageAction(
                                label='message1',
                                text='message text1'
                            ),
                            URIAction(
                                label='uri1',
                                uri='http://example.com/1'
                            )
                        ]),
                        CarouselColumn(title='this is menu2', text='description2', actions=[
                            PostbackAction(
                                label='postback2',
                                display_text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageAction(
                                label='message2',
                                text='message text2'
                            ),
                            URIAction(
                                label='uri2',
                                uri='http://example.com/2'
                            )
                        ]),
                    ])
                    template_message = TemplateSendMessage(alt_text='Carousel alt text', template=carousel_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                    continue
                elif '@img_carousel' in msg:
                    image_carousel_template = ImageCarouselTemplate(columns=[
                        ImageCarouselColumn(
                            image_url=IMG_1,
                            action=PostbackAction(
                                label='postback1',
                                display_text='postback text1',
                                data='action=buy&itemid=1'
                            )
                        ),
                        ImageCarouselColumn(
                            image_url=IMG_2,
                            action=PostbackAction(
                                label='postback2',
                                display_text='postback text2',
                                data='action=buy&itemid=2'
                            )
                        )
                    ])
                    template_message = TemplateSendMessage(alt_text='ImageCarousel alt text', template=image_carousel_template)
                    line_bot_api.reply_message(event.reply_token, template_message)
                    continue
                elif msg.startswith('@flex'):
                    flex_message = FlexSendMessage(
                        alt_text='hello',
                        contents={
                            'type': 'bubble',
                            'direction': 'ltr',
                            'hero': {
                                'type': 'image',
                                'url': IMG_1,
                                'size': 'full',
                                'aspectRatio': '20:13',
                                'aspectMode': 'cover',
                                'action': { 'type': 'uri', 'uri': 'http://example.com', 'label': 'label' }
                            }
                        }
                    )
                    template_message = TemplateSendMessage(alt_text='flex_message', template=flex_message)
                    line_bot_api.reply_message(event.reply_token, template_message)
                    continue
                
                
                
                
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
                elif msg.startswith('樂透對獎'):
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text='https://yibot.herokuapp.com/lottery/'))
                    continue
                else:
                    continue
                
                imgURL = findMeme(msg)
                if not imgURL:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextMessage(text='查無圖片')
                    )
                    line_bot_api.push_message(replyID, StickerSendMessage(package_id='2', sticker_id='38'))
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
        if not user.exists():
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
    
    
    
