from django.db import transaction
from linebot.api import LineBotApi
from linebot.models.messages import TextMessage

from lineBot.models import LineUser
from todoList.models import Item
from yiBot.settings import LINE_CHANNEL_ACCESS_TOKEN
from django.http.response import HttpResponse


# Create your views here.
def todoList(replyID, command, msg=None):
    try:
        user = LineUser.objects.get(lineID=replyID, chatFrom='user')
    except:
        return ''
    
    if command == 'show':
        response = itemResponse(user)
        if not response:
            return '目前無任何待辦事項！'
        return response    
    elif command == 'createItem':
        return createItem(user, msg)
    elif command == 'doneItem':
        return doneItem(user, msg)
    elif command == 'clearItem':
        return clearItem(user)
#     return render(request, 'todoList/todoList.html', {})


def createItem(user, content):
    item = Item()
    item.user = user
    item.content = content
    item.order_num = maxOrderNum(user)
    item.save()
    
    return '{0} 已新增至待辦清單'.format(content)
    

@transaction.atomic
def maxOrderNum(user):
    item = Item.objects.filter(user=user).exclude(order_num=-1).last()    # model ordering有按照order_num排序，故最後一筆為最大
    if item:
        return item.order_num + 1
    return 1
    
    
def doneItem(user, order_num):
    try:
        item = Item.objects.get(user=user, order_num=order_num, done=False)
    except:
        return '編號不存在或格式錯誤 \n 格式：@done + 編號 \n 範例：@done 3'
    
    item.done = True
    item.save()
    
    reSortItem(user)
    return '{0} 已從清單上移除'.format(item.content)


def reSortItem(user):
    #===========================================================================
    # 當有事件完成後，重新排序編號
    # 例：原有項目1234，使用者刪除項目2後，要將原有項目3、4更新至2、3
    #===========================================================================
    items = Item.objects.filter(user=user, done=False)
    
    for index, item in enumerate(items, 1):
        item.order_num = index
        item.save()
    
    
def clearItem(user):
    items = Item.objects.filter(user=user, done=False)
    itemList = []
    for item in items:
        itemList.append('{0}. {1}'.format(item.order_num, item.content))
    
    items.update(done=True, order_num=-1)
    return '已移除以下清單： \n {0}'.format('\n'.join(itemList))
    
    
def itemResponse(user):
    items = Item.objects.filter(user=user, done=False)
    response = ['待辦事項如下：\n(輸入 @done + 項目編號即可確認完成) \n']
    for item in items:
        response.append('{0}. {1}'.format(item.order_num, item.content))
    
    if not items.exists():
        return None
    return '\n'.join(response)


def notifyTodo(request):
    #===========================================================================
    # cronJob 每日特定時間提醒使用者目前剩餘的待辦項目
    #===========================================================================
    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    
    users = LineUser.objects.filter(chatFrom='user')
    for user in users:
        notify = itemResponse(user)
        if notify:
            line_bot_api.push_message(user.lineID, TextMessage(text=notify))
        
    return HttpResponse(True)
        


