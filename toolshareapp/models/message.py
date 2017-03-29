from datetime import datetime
from django.db import models
from toolshareapp.models.user import User

class Message(models.Model):
    
    class Meta:
        app_label='toolshareapp'
        
    text = models.TextField(max_length=1000)
    subject = models.CharField(max_length=200)
    from_user = models.ForeignKey(User, related_name='message_set_from_user')
    to_user = models.ForeignKey(User, related_name='message_set_to_user')
    time = models.DateTimeField(auto_now_add = True)
    viewed = models.BooleanField()
    answer_to = models.ForeignKey('self', null = True)
    active = models.BooleanField()
    
    def deactivate(self):
        self.active = False
        
    def create(self):
        self.viewed = False