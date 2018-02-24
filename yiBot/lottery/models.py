from django.db import models

# Create your models here.
class WinningNumbers(models.Model):
    normalNums = models.CharField(max_length=255)                         # 普通號可能有6碼或更多（春節加碼有十碼）已逗號分隔
    specialNum = models.CharField(max_length=2, blank=True, null=True)    # 特別號可能沒有或有一個（春節加碼沒有特別號；用字元型態是因為要保留數字0）
    lotteryType = models.CharField(max_length=50)                         # 這組中獎號碼的樂透類型為何（大樂透or威力彩...等，但目前只做大樂透）
    drawNo = models.CharField(max_length=50)                              # 這組中獎號碼是第幾期（叫drawNo是因為大樂透官方期數就叫做ddlDrawNo）
    drawDate = models.DateField()                                         # 開獎日期
    
    def __str__(self):
        return self.drawNo

    class Meta:
        ordering = ['drawNo', 'id']
