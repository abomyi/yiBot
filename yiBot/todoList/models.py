from django.db import models
from lineBot.models import LineUser

# Create your models here.
class Item(models.Model):
    user = models.ForeignKey(LineUser)
    content = models.TextField()
    order_num = models.IntegerField()
    create_date_time = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)    # 是否完成，若為True則order_num為0
    
    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['order_num']
        
        
