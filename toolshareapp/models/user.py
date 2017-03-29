from django.db import models

from toolshareapp.models.user_role import UserRole
from django.contrib.auth.models import User as SystemUser
from datetime import datetime

class User(models.Model):
    
    class Meta:
        app_label = 'toolshareapp'
    
    email = models.EmailField(max_length = 500, unique = True)
    name = models.CharField(max_length = 50)
    lastname = models.CharField(max_length = 50)
    password = models.CharField(max_length = 500)
    registration_date = models.DateTimeField()
    house_number = models.CharField(max_length = 5)
    street_name = models.CharField(max_length = 500)
    zip_code = models.CharField(max_length = 5)
    phone_number = models.CharField(max_length = 10)
    last_login_date = models.DateTimeField()
    preferred_pickup_location = models.TextField(max_length = 500)
    email_notifications = models.BooleanField()
    preferred_contact_method = models.CharField(max_length = 500)
    active = models.BooleanField()
    role = models.CharField(max_length=100)
    picture = models.FileField(upload_to = 'user')
    
    def __str__(self):
        return self.name + ' ' + self.lastname
    
    def deactivate(self):
        self.active = False        

    def register(self, system_user):
        self.id = system_user.id
        self.last_login_date = datetime.now()
        self.role = UserRole.Regular
        self.active = True
        self.registration_date = datetime.now()