from django.db.models import Q

from toolshareapp.models import Tool
from toolshareapp.models import ToolStatus
from toolshareapp.models import User
from toolshareapp.services.notification_service import NotificationService
from toolshareapp.services.email_service import EmailService
from toolshareapp.services.reservation_service import ReservationService

notificationService = NotificationService()
emailService = EmailService()
reservationService = ReservationService()

class ToolHasReservationsError(Exception):
    def __init__(self, msg):
        self.msg = msg

class ToolService:
    
    def send_email_if_notification_enabled(self, template, subject, to, reservation):            
        if to.email_notifications:
            emailService.send_email(template, subject, to.email, reservation)   

    def register(self, tool):
        tool.status = ToolStatus.Available
        tool.active = True
        
        if tool.shed is not None and tool.shed.coordinator != tool.owner:
            self.send_email_if_notification_enabled('inclusion_request',
                                               'New inclusion request for your shed',
                                               tool.shed.coordinator,
                                               tool)
            notificationService.create("/toolshare/shed/requests/",
                                   tool.shed.coordinator.id,
                                   "There is a new tool inclusion request for your shed")
        
            tool.requested_shed = tool.shed
            tool.shed = None
            
        tool.save()

    def update(self, tool, user_id):        
        orig = Tool.objects.get(id = tool.id)
                
        if orig.shed_id != tool.shed_id:
            
            if reservationService.get_reservations_by_tool(tool.id): # if tool can change location
                raise ToolHasReservationsError("Cannot change this tool's location. It has pending reservations.")
            
            if tool.shed_id and tool.shed.coordinator_id != user_id:
                tool.requested_shed_id = tool.shed_id
                tool.shed_id = orig.shed_id
                
                self.send_email_if_notification_enabled('inclusion_request',
                                               'New inclusion request for your shed',
                                               tool.shed.coordinator,
                                               tool)
                notificationService.create("/toolshare/shed/requests/",
                                   tool.shed.coordinator.id,
                                   "There is a new tool inclusion request for your shed")
        
            else:
                tool.requested_shed_id = None                
        
        tool.save()

    def deregister(self, tool_id):
        tool = Tool.objects.get(id = tool_id)
        tool.deactivate()
        tool.save()
        reservations = reservationService.get_reservations_by_tool(tool_id)
        
        for reservation in reservations:
            reservationService.cancel_lend(reservation.id, reservation.tool.owner_id)
            notificationService.create("/toolshare/reservation/", reservation.user_id,
                                       "The " + tool.name + " you had a reservation for, has been deregistered.")
            self.send_email_if_notification_enabled('cancel_lend',
                                           "The " + tool.name + " you had a reservation for, has been deregistered.",
                                           reservation.user,
                                           reservation)
        
    def withhold(self, tool_id):
        tool = Tool.objects.get(id = tool_id)        
        tool.make_unavailable()        
        tool.save()
        
        reservations = reservationService.get_reservations_by_tool(tool_id)
        
        for reservation in reservations:
            reservationService.cancel_lend(reservation.id, reservation.tool.owner_id)
    
    def release(self, tool_id):
        tool = Tool.objects.get(id = tool_id)
        tool.make_available()
        tool.save()

    def get_tools_owned_by_user(self, user_id):
        tools = Tool.objects.filter(owner_id = user_id).filter(active = True)
        return tools
    
    def get_tools_in_users_shed(self, search_term, user_id):
        tools = Tool.objects.filter(shed__coordinator_id = user_id).filter(active = True)
        
        if search_term:
            tools = tools.filter(
                Q(name__contains = search_term) |
                Q(description__contains = search_term) |
                
                Q(categories__description__contains = search_term) |
                
                Q(owner__name__contains = search_term) |
                Q(owner__lastname__contains = search_term) |                
                Q(owner__street_name__contains = search_term)
            )
            
        return tools
    
    def get_all_tools(self):
        return Tool.objects.all()
    
    def get_tools(self, search_term, user_id):
        user = User.objects.get(id=user_id)
        tools = Tool.objects.filter(active = True).filter(owner__zip_code = user.zip_code).exclude(status = ToolStatus.Unavailable)
        
        if search_term:
            tools = tools.filter(
                Q(name__contains = search_term) |
                Q(description__contains = search_term) |
                
                Q(categories__description__contains = search_term) |
                
                Q(owner__name__contains = search_term) |
                Q(owner__lastname__contains = search_term) |                
                Q(owner__street_name__contains = search_term)
            )
        
        return tools
    
    def get_tool(self, tool_id):
        return Tool.objects.get(id = tool_id)
    