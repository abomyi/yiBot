from django.urls import path

from lottery import views

app_name = 'lottery'
urlpatterns = [
    path('getLotteryNumbers/', views.getLotteryNumbers, name='getLotteryNumbers'),
    path('', views.lottery, name='lottery'),
]
