from django.db import models
from toolshareapp.models.user import User

class Notification(models.Model):
    
    class Meta:
        app_label='toolshareapp'
        
    link = models.CharField(max_length = 100)
    user = models.ForeignKey(User)
    viewed = models.BooleanField()
    text = models.CharField(max_length = 500)