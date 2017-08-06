from django.conf.urls import url

from lineBot import views


urlpatterns = [
    url(r'^$', views.lineBot, name='lineBot'),
]
