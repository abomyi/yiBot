from django.db import models

# Create your models here.
class Item(models.Model):
#     user = models.ForeignKey()
    content = models.TextField()
    order_num = models.IntegerField()
    create_date_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
    class Meta:
        ordering = ['create_date_time']
        
        
