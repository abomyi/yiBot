from django.contrib import admin
from lineBot.models import LineUser, Card


class LineUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'chatFrom', 'lineID', 'commander']
    list_filter = ['chatFrom']


class CardAdmin(admin.ModelAdmin):
    list_display = ['name', 'weight']


# Register your models here.
admin.site.register(LineUser, LineUserAdmin)
admin.site.register(Card, CardAdmin)