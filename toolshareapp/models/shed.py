from django.db import models

from toolshareapp.models.user import User

class Shed(models.Model):
    
    class Meta:
        app_label = 'toolshareapp'

    house_number = models.CharField(max_length = 5)
    street_name = models.CharField(max_length = 500)
    active = models.BooleanField()
    
    open_from = models.TimeField()
    open_to = models.TimeField()
    
    coordinator = models.ForeignKey(User, unique = True)
    
    def __str__(self):
        return self.house_number + ' ' +  self.street_name
    
    def deactivate(self):
        self.active = False