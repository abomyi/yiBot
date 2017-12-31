from django.contrib import admin

from todoList.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ['line_user', 'order_num', 'content', 'done']
    list_filter = ['user__name']
    
    def line_user(self, obj):
        return obj.user.name
    
    
# Register your models here.
admin.site.register(Item, ItemAdmin)
