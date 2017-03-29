from django.test import TestCase
from datetime import datetime
from toolshareapp.models.reservation import *
from toolshareapp.models.reservation_status import *
from toolshareapp.models.user_role import *
from toolshareapp.models.user import *
from toolshareapp.services.user_service import *
from django.contrib.auth.models import User as SystemUser
    


class UserTest(TestCase):

    def test_user_has_right_id(self):
        """Created user has the same id that the corresponding django auth user"""
        #arrange
        test_user = User.objects.create(password="123456", email="theuser@gmail.com", name="Catherine", lastname="Ramirez",
        registration_date=datetime.now().date(), house_number="1A", street_name="coolstreet", phone_number="5859571564",
        last_login_date=datetime.now(),preferred_pickup_location="my house", email_notifications=True,
        preferred_contact_method="Phone", role = UserRole.Regular)
        
        auth_user = SystemUser.objects.create_user(test_user.email,test_user.email,test_user.password)
        
        #act
        test_user.register(auth_user)
        
        #assert
        self.assertEqual(auth_user.id, test_user.id)
        
        #this probably shouldn't happen
        auth_user.delete()
    
    def test_user_is_registered(self):
        """User is properly registered"""
        #arrange
        test_user = User.objects.create(password="123456", email="theuser@gmail.com", name="Catherine", lastname="Ramirez",
        registration_date=datetime.now().date(), house_number="1A", street_name="coolstreet", phone_number="5859571564",
        last_login_date=datetime.now(),preferred_pickup_location="my house", email_notifications=True,
        preferred_contact_method="Phone", role = UserRole.Regular, active = True)
        
        service = UserService()
        
        #act
        try:
            service.register(test_user)
            #assert
            SystemUser.objects.get(username__exact=test_user.email)
        except SystemUser.DoesNotExist:
            self.fail("The user was not registered!")   
        
        
    def test_user_is_deactivated(self):
        
        #arrange
        test_user = User.objects.create(password="123456", email="theuser@gmail.com", name="Catherine", lastname="Ramirez",
        registration_date=datetime.now().date(), house_number="1A", street_name="coolstreet", phone_number="5859571564",
        last_login_date=datetime.now(),preferred_pickup_location="my house", email_notifications=True,
        preferred_contact_method="Phone", role = UserRole.Regular, active = True)
        
        service = UserService()
        new_user = service.register(test_user)
        
        #act
        new_user = service.deactivate(new_user.id)
        
        #assert
        self.assertFalse(new_user.active)
        
        
    
    