from django.db import models

from toolshareapp.models.tool_status import ToolStatus
from toolshareapp.models.user import User
from toolshareapp.models.tool import Tool
from toolshareapp.models.reservation_status import ReservationStatus

from datetime import date

class Reservation(models.Model):
    
    class Meta:
        app_label = 'toolshareapp'
    
    start_date = models.DateField()
    end_date = models.DateField()    
    status = models.CharField(max_length = 100)
    user = models.ForeignKey(User)
    tool = models.ForeignKey(Tool)
    pickup_arrangement = models.CharField(max_length = 200)
    comment = models.CharField(max_length = 200, null = True)
    
    def __str__(self):
        return self.start_date.strftime('%m/%d/%Y') + ' - ' + self.end_date.strftime('%m/%d/%Y')
    
    def approve_borrower(self): # only aplicable status: Pending_approval
        if self.start_date == date.today():
            self.status = ReservationStatus.Ongoing
        else:
            self.status = ReservationStatus.Awating_for_start_date
    
    def reject_borrower(self): # only aplicable status: Pending_approval
        self.status = ReservationStatus.Cancelled
    
    def request_borrow(self):
        if self.tool.owner.id == self.user_id or self.tool.shed is not None:
            self.approve_borrower()
        else:
            self.status = ReservationStatus.Pending_approval
            
    def set_pickup_arrangement(self, pickup):
        self.pickup_arrangement = pickup    
    
    def return_tool(self): # only aplicable status: Pending_return
        self.status = ReservationStatus.Pending_return_acknowledge
        self.tool.status = ToolStatus.Available
    
    def acknowledge_tool_return(self): # only aplicable status: Pending_return
        self.status = ReservationStatus.Returned
    
    # When the lender requests cacelation OR the cancelation is triggered by
    # shed coordinator approving an inclusion request
    def cancel_lend(self):
        if self.status == ReservationStatus.Ongoing:
            self.status = ReservationStatus.Pending_return
        else: # status will be Awating_for_start_date when lender requests cacelation.
            self.status = ReservationStatus.Cancelled
            
    # When the Borrower requests cacelation
    def cancel_borrow(self):        
        if self.status in [ReservationStatus.Pending_approval, ReservationStatus.Awating_for_start_date]:
            self.status = ReservationStatus.Cancelled