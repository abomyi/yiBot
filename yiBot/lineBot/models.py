from django.db import models

# Create your models here.
class LineUser(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)  #群組、房間沒辦法抓到名稱
    chatFrom = models.CharField(max_length=50)                      #來源：user、group、room
    lineID = models.CharField(max_length=255)                       #ID 非自行設定的好友ID，而是line的傳訊ID
#     statusMSG = models.TextField(blank=True, null=True)           #可能沒有簽名檔(用不到 沒意義)
    commander = models.BooleanField(default=False)                  #是否能夠下特殊指令
    
    def __str__(self):
        return self.lineID


class Card(models.Model):
    name = models.CharField(max_length=150)
    weight = models.FloatField(default=0)

    def __str__(self):
        return self.name
