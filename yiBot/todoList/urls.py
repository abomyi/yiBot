from django.urls import path

from todoList import views

app_name = 'todoList'
urlpatterns = [
    path('', views.todoList, name='todoList'),
]
