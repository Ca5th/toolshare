from django.test import TestCase
from datetime import datetime
from toolshareapp.models.reservation import *
from toolshareapp.models.reservation_status import *
from toolshareapp.models.user_role import *
from toolshareapp.models.user import *
from django.contrib.auth.models import User as SystemUser



class ReservationTest(TestCase):        

    def test_reservation_is_approved(self):
        #arrange
        test_user = User.objects.create(password="123456", email="theuser", name="Catherine", lastname="Ramirez",
        registration_date=datetime.now().date(), house_number="1A", street_name="coolstreet", phone_number="5859571564",
        last_login_date=datetime.now(),preferred_pickup_location="my house", email_notifications=True,
        preferred_contact_method="Phone", role = UserRole.Regular)
        
        test_tool = Tool.objects.create(name = 'test tool 1',
                    description = 'tool description 1',
                    active = True,
                    status = ToolStatus.Available,
                    owner = test_user)

        reservation = Reservation.objects.create(start_date = datetime.now().date(), tool = test_tool,
        end_date = datetime.now().date(), status = ReservationStatus.Pending_approval, user = test_user)
        auth_user = SystemUser.objects.create_user(test_user.email,test_user.email,test_user.password)             
        
        #Act
        reservation.approve_borrower()
        
        #Assert
        self.assertEqual(reservation.status, "Awaiting start date")
        
        #nope
        auth_user.delete()