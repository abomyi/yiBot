from django.contrib import admin
from lottery.models import WinningNumbers


class WinningNumbersAdmin(admin.ModelAdmin):
    list_display = ['drawNo', 'drawDate', 'normalNums', 'specialNum', 'lotteryType']


# Register your models here.
admin.site.register(WinningNumbers, WinningNumbersAdmin)
