from django.shortcuts import render, redirect, get_object_or_404

from todoList.models import Item
from django.db import transaction
from lineBot.models import LineUser


# Create your views here.
def todoList(replyID, command, msg=None):
    try:
        user = LineUser.objects.get(lineID=replyID, chatFrom='user')
    except:
        return ''
    
    if command == 'show':
        items = Item.objects.filter(user=user, done=False)
        response = []
        for index, item in enumerate(items, 1):
            response.append('{0}. {1}'.format(index, item.content))
        
        if not response:
            return '目前無任何待辦事項！'
        return '\n'.join(response)
    
    elif command == 'createItem':
        createItem(user, msg)
    elif command == 'doneItem':
        pass
        
    
#     return render(request, 'todoList/todoList.html', {})


def createItem(user, content):
    item = Item()
    item.user = user
    item.content = content
    item.order_num = max_order_num(user)
    item.save()
    

@transaction.atomic
def max_order_num(user):
    item = Item.objects.filter(user=user).last()    # model ordering有按照order_num排序，故最後一筆為最大
    if item:
        return item.order_num + 1
    return 1
    
    
    
    
    
