from django.conf.urls import url

from lottery import views


urlpatterns = [
    url(r'^getLotteryNumbers/$', views.getLotteryNumbers, name='getLotteryNumbers'),
    url(r'^$', views.lottery, name='lottery'),
]
