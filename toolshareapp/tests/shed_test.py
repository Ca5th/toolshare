from django.test import TestCase
from toolshareapp.models.shed import *
from toolshareapp.services.shed_service import *
from datetime import datetime
from toolshareapp.models.user_role import *
from toolshareapp.models.user import *

class ShedTest(TestCase):
    
    def test_shed_is_registered(self):
        #arrange
        test_user = User.objects.create(password="123456", email="theuser@gmail.com", name="Catherine", lastname="Ramirez",
                                        registration_date=datetime.now().date(), house_number="1A", street_name="coolstreet", phone_number="5859571564",
                                        last_login_date=datetime.now(),preferred_pickup_location="my house", email_notifications=True,
                                        preferred_contact_method="Phone", role = UserRole.Regular, active = True)
        
        test_shed = Shed.objects.create(house_number="B10", street_name="Sloth Street", coordinator=test_user,
                                        open_from="4:00", open_to="5:00")
        
        service = ShedService()
        
        #act
        try:
            created_shed = service.register(test_shed)
            Shed.objects.get(id = created_shed.id)
        except Shed.DoesNotExist:
            self.fail("The shed was not registered.")
    
    def test_shed_is_updated(self):
        #arrange
        test_user = User.objects.create(password="123456", email="theuser@gmail.com", name="Catherine", lastname="Ramirez",
                                        registration_date=datetime.now().date(), house_number="1A", street_name="coolstreet", phone_number="5859571564",
                                        last_login_date=datetime.now(),preferred_pickup_location="my house", email_notifications=True,
                                        preferred_contact_method="Phone", role = UserRole.Regular, active = True)
        
        test_shed = Shed.objects.create(house_number="B10", street_name="Sloth Street", coordinator=test_user,
                                        open_from="4:00", open_to="5:00")
        test_shed.house_number = "A11"
        
        service = ShedService()
        
        created_shed = service.register(test_shed)
        
        #act
        service.update(test_shed)
        updated_shed = Shed.objects.get(id=created_shed.id)
        
        #assert
        self.assertEqual("A11" , updated_shed.house_number)
