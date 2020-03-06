from django.urls import path

from lineBot import views
from todoList import views as todoViews


app_name = 'lineBot'
urlpatterns = [
    path('notifyTodo/', todoViews.notifyTodo, name='notifyTodo'),
    path('', views.lineBot, name='lineBot'),
]
