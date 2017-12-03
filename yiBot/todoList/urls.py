from django.conf.urls import url

from todoList import views


urlpatterns = [
    url(r'^$', views.todoList, name='todoList'),
]
