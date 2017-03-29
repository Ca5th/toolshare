from datetime import datetime
from datetime import date
from django.db.models import Q

from toolshareapp.models import Reservation, ReservationStatus, ReservationEvent, ReservationHistory
from toolshareapp.services.notification_service import NotificationService
from toolshareapp.services.email_service import EmailService
#things only python ninjas do!
#http://stackoverflow.com/questions/739654/how-can-i-make-a-chain-of-function-decorators-in-python
#This is a decorator for logging the reservation operations.
def log_operation(event):
    def my_decorator(func):
        def decorated(*args):
            
            #import pdb;pdb.set_trace()
            
            res = func(*args)
            
            obj, reservation_id, logged_user_id, *other = args #unpacking the arguments like a boss!

            if event == ReservationEvent.Rejection:
                history_entry = ReservationHistory(
                    event_date = datetime.now(),
                    event = event,
                    user_id = logged_user_id,
                    rejection_reasons = other[0])
            else:
                history_entry = ReservationHistory(
                    event_date = datetime.now(),
                    event = event,
                    user_id = logged_user_id)
            
            res.reservationhistory_set.add(history_entry)
            
        return decorated
    return my_decorator

notificationService = NotificationService()
emailService = EmailService()

class ReservationService():
    
    #def log_operation(self, reservation, event, user_id):
    #    reservation.reservationhistory_set.create(
    #        event_date = datetime.now(),
    #        event = event,
    #        user_id = user_id
    #    )
    
    def send_email_if_notification_enabled(self, template, subject, to, reservation):            
        if to.email_notifications:
            emailService.send_email(template, subject, to.email, reservation)    

    def get_reservation(self, reservation_id):
        return Reservation.objects.get(id=reservation_id)

    @log_operation(event = ReservationEvent.Approval)
    def approve_borrower(self, reservation_id, logged_user_id, pickup):
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.approve_borrower()
        reservation.set_pickup_arrangement(pickup)
        
        reservation.save()
        
        notificationService.create("/toolshare/reservation/detail/"+str(reservation_id),
                                   reservation.user.id,
                                   "Your reservation has been approved.")
        
        reservation.pickup = pickup
        
        self.send_email_if_notification_enabled('approval',
                                                'Your reservation has been approved',
                                                reservation.user,
                                                reservation)
        
        return reservation

    @log_operation(event = ReservationEvent.Rejection)
    def reject_borrower(self, reservation_id, logged_user_id, rejection_reason):
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.reject_borrower()
        reservation.save()
        
        notificationService.create("/toolshare/reservation/detail/"+str(reservation_id), reservation.user.id,
                                   "Your reservation has been rejected.")
        
        reservation.rejection_reason = rejection_reason #this line makes me sad
        
        self.send_email_if_notification_enabled('rejection',
                                           'Your reservation request has been rejected',
                                           reservation.user,
                                           reservation)
        
        return reservation
    
    @log_operation(event = ReservationEvent.Creation)
    def request_borrow(self, reservation, logged_user_id):
        reservation.request_borrow()        
        reservation.save()
            
        if reservation.tool.shed is None:
            send_to = reservation.tool.owner
        else:
            send_to = reservation.tool.shed.coordinator
        
        if reservation.tool.owner.id != reservation.user.id:
            if reservation.status == ReservationStatus.Pending_approval: 
                self.send_email_if_notification_enabled('creation',
                                                   'Your tool has been requested',
                                                   send_to,
                                                   reservation)
                notificationService.create("/toolshare/reservation/detail/" + str(reservation.id),
                                       send_to.id,
                                       "A reservation has been requested for you tool")
                
            else:
                self.send_email_if_notification_enabled('approval',
                                                   'Your reservation has been approved',
                                                   reservation.user,
                                                   reservation)
                notificationService.create("/toolshare/reservation/detail/" + str(reservation.id),
                                        reservation.user.id,
                                       "Your reservation has been approved'")
            
        return reservation
    
    @log_operation(event = ReservationEvent.Return)
    def return_tool(self, reservation_id, logged_user_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.return_tool()
        reservation.save()
        
        if reservation.tool.shed is None:
            send_to = reservation.tool.owner
        else:
            send_to = reservation.tool.shed.coordinator
            
        notificationService.create("/toolshare/reservation/detail/"+str(reservation_id),
                                   send_to.id,
                                   "Your tool has been returned.")
        
        self.send_email_if_notification_enabled('return',
                                           'Your tool has been returned',
                                           send_to,
                                           reservation)
        
        return reservation
    
    @log_operation(event = ReservationEvent.Return_acknowledge)
    def acknowledge_tool_return(self, reservation_id, logged_user_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.acknowledge_tool_return()
        reservation.save()
        
        return reservation
    
    @log_operation(event = ReservationEvent.Cancelation)
    def cancel_lend(self, reservation_id, logged_user_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.cancel_lend()
        reservation.save()
        
        notificationService.create("/toolshare/reservation/detail/"+str(reservation_id),
                                   reservation.user.id,
                                   "Your reservation has been canceled.")
        
        self.send_email_if_notification_enabled('cancel_lend',
                                           'The lender has canceled your reservation',
                                           reservation.user,
                                           reservation)
        
        return reservation
    
    @log_operation(event = ReservationEvent.Cancelation)
    def cancel_borrow(self, reservation_id, logged_user_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.cancel_borrow()
        reservation.save()
        
        if reservation.tool.shed is None:
            send_to = reservation.tool.owner
        else:
            send_to = reservation.tool.shed.coordinator
            
        notificationService.create("/toolshare/reservation/detail/"+str(reservation_id),
                                   send_to.id,
                                   "The reservation for your tool:" + reservation.tool.name + "has been canceled.")
        
        self.send_email_if_notification_enabled('cancel_borrow',
                                           'The borrower has canceled their reservation',
                                           send_to,
                                           reservation)
        
        return reservation
    
    @log_operation(event = ReservationEvent.Time_start)
    def reservation_time_start(self, reservation_id, user_id):
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.status = ReservationStatus.Ongoing
        reservation.save()
        return reservation
    
    @log_operation(event = ReservationEvent.Time_end)
    def reservation_time_end(self, reservation_id, user_id):
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.status = ReservationStatus.Pending_return
        reservation.save()
        return reservation
    
    #get reservations the user made
    def get_reservations_by_user(self, user_id):
        reservations = Reservation.objects.filter(user_id = user_id).exclude(status=ReservationStatus.Cancelled).exclude(status=ReservationStatus.Returned)
        return reservations
    
    #get reservations made for the user's tools
    def get_reservations_by_owner(self, user_id):
        reservations = Reservation.objects.filter(Q(tool__owner_id = user_id, tool__shed=None) | Q(tool__shed__coordinator_id = user_id)).\
        exclude(status=ReservationStatus.Cancelled).exclude(status=ReservationStatus.Returned).\
        order_by('-id')
        return reservations
    
    def get_reservations_by_tool(self, tool_id):
        reservations = Reservation.objects\
                             .filter(tool__id = tool_id)\
                             .exclude(status = ReservationStatus.Cancelled)\
                             .exclude(status = ReservationStatus.Returned)
        
        return reservations
    
    def get_reservation_history(self, reservation_id):
        return ReservationHistory.objects.filter(reservation_id=reservation_id).order_by('-event_date')
    
    def get_reserved_dates_for_tool(self, tool_id):
        alive_reservations = Reservation.objects\
                             .filter(tool__id = tool_id)\
                             .filter(end_date__gte = date.today())\
                             .exclude(status = ReservationStatus.Cancelled)\
                             .exclude(status = ReservationStatus.Returned)
        
        reserved_dates_start = alive_reservations.values_list('start_date', flat=True)
        reserved_dates_end = alive_reservations.values_list('end_date', flat=True)
        
        return reserved_dates_start, reserved_dates_end
    