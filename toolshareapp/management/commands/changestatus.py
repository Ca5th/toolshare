from django.core.management.base import BaseCommand, CommandError
from toolshareapp.models import Reservation
from toolshareapp.models import ReservationStatus
from toolshareapp.models import ReservationEvent
from toolshareapp.models import ReservationHistory
from toolshareapp.services import ReservationService
from toolshareapp.services import UserService

from datetime import datetime

reservationService = ReservationService()
userService = UserService()

class Command(BaseCommand):
    help = 'Changes status of the reservation'

    def handle(self, *args, **options):
        user = userService.get_user_by_email("toolshare.team.d@gmail.com")
        
        reservations = Reservation.objects.filter(start_date=datetime.now().date())\
                                          .filter(status = ReservationStatus.Awating_for_start_date)
        
        for reservation in reservations:
            if reservation.status != ReservationStatus.Ongoing:
                reservationService.reservation_time_start(reservation.id, user.id)
                self.stdout.write('Successfully changed reservation "%s" status' % reservation.id)
        
        reservations = Reservation.objects.filter(end_date=datetime.now().date())\
                                          .filter(status = ReservationStatus.Ongoing)
        
        for reservation in reservations:
            if reservation.status != ReservationStatus.Pending_return:
                reservationService.reservation_time_end(reservation.id, user.id)
                self.stdout.write('Successfully changed reservation "%s" status' % reservation.id)
            
    
            
        