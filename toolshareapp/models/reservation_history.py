from django.db import models

from toolshareapp.models.reservation import Reservation
from toolshareapp.models.reservation_event import ReservationEvent
from toolshareapp.models.user import User

class ReservationHistory(models.Model):
    
    class Meta:
        app_label = 'toolshareapp'
    
    event_date = models.DateTimeField()
    
    reservation = models.ForeignKey(Reservation)    
    event = models.CharField(max_length=100)
    user = models.ForeignKey(User)
    rejection_reasons = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.event_date.strftime('%m/%d/%Y')