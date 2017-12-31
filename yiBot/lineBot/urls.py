from django.conf.urls import url

from lineBot import views
from todoList import views as todoViews

urlpatterns = [
    url(r'^notifyTodo/$', todoViews.notifyTodo, name='notifyTodo'),
    url(r'^$', views.lineBot, name='lineBot'),
]
