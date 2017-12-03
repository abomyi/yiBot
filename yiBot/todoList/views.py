from django.shortcuts import render, redirect

from todoList.models import Item


# Create your views here.
def todoList(request):
    
    return render(request, 'todoList/todoList.html', {})


def createItem(request):
    if request.method=='GET':
        return redirect('todoList:todoList')
    
    item = Item()
    item.content = request.POST.get('content')
    item.save()