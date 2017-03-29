from django.test import TestCase
from toolshareapp.services.notification_service import *
from toolshareapp.services.user_service import *
from datetime import datetime
from toolshareapp.models import *

class NotificationTest(TestCase):
    
    def test_notification_is_created(self):
        #arrange
        test_user = User.objects.create(password="123456", email="theuser@gmail.com", name="Catherine", lastname="Ramirez",
                                        registration_date=datetime.now().date(), house_number="1A", street_name="coolstreet", phone_number="5859571564",
                                        last_login_date=datetime.now(),preferred_pickup_location="my house", email_notifications=True,
                                        preferred_contact_method="Phone", role = UserRole.Regular, active = True)
        
        service = NotificationService()
            
        #act and assert
        try:
            service.create("toolshareapp/reservation/detail/1", test_user.id, "you have a new notification")
            created_notification = Notification.objects.get(link__exact="toolshareapp/reservation/detail/1",
                                                        user_id = test_user.id,
                                                        text__exact="you have a new notification")
        except Notification.DoesNotExist:
            self.fail("The notification was not registered.")
            
    
    def test_notifications_are_retrieved(self):
        #arrange
        test_user = User.objects.create(password="123456", email="theuser@gmail.com", name="Catherine", lastname="Ramirez",
                                        registration_date=datetime.now().date(), house_number="1A", street_name="coolstreet", phone_number="5859571564",
                                        last_login_date=datetime.now(),preferred_pickup_location="my house", email_notifications=True,
                                        preferred_contact_method="Phone", role = UserRole.Regular, active = True)
        
        service = NotificationService()
        service.create("toolshareapp/reservation/detail/1", test_user.id, "you have a new notification")
            
        #act 
        notifications = service.get_notifications_by_user(test_user.id)
        
        #assert
        self.assertEqual(1, notifications.count())