from django.contrib import admin
from lineBot.models import LineUser


class LineUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'chatFrom', 'lineID', 'commander']
    list_filter = ['chatFrom']

# Register your models here.
admin.site.register(LineUser, LineUserAdmin)