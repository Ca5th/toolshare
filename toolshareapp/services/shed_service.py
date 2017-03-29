from toolshareapp.models import Shed
from toolshareapp.models import User
from toolshareapp.models import Tool
from toolshareapp.services.tool_service import ToolService
from toolshareapp.services.notification_service import NotificationService
from toolshareapp.services.email_service import EmailService
from toolshareapp.services import ReservationService

from django.db.utils import IntegrityError

toolService = ToolService()
notificationService = NotificationService()
emailService = EmailService()
reservationService = ReservationService()

class ShedService():
    
    def send_email_if_notification_enabled(self, template, subject, tool):
        if tool.owner.email_notifications:
            emailService.send_email_tool(template, subject, tool)    
    
    def register(self, shed):        
        try:
            shed.active = True
            shed.save()
        except IntegrityError:
            old_shed = Shed.objects.filter(coordinator_id = shed.coordinator_id)[0]
            shed.id = old_shed.id            
            shed.save()
            
        return shed
    
    def update(self, shed):
        shed.save()    
    
    def delete(self, shed_id):
        shed = Shed.objects.get(id = shed_id)
        shed.deactivate()
        shed.save()
        
    def get_shed(self, shed_id):
        return Shed.objects.get(id=shed_id)    
        
    def get_sheds(self, user_id):
        user = User.objects.get(id=user_id)
        sheds = Shed.objects.filter(active = True).filter(coordinator__zip_code = user.zip_code)
        
        return sheds
    
    def get_shed_by_user(self, user_id):
        try:
            return Shed.objects.filter(coordinator_id = user_id).filter(active = True)[0]
        except IndexError:
            raise Shed.DoesNotExist
    
    def deregister(self, shed_id):
        shed = Shed.objects.get(id = shed_id)
        shed.deactivate()
        shed.save()
        
        tools = toolService.get_tools_in_users_shed(None, shed.coordinator)
        
        for tool in tools:
            notificationService.create("/toolshare/tool/owned/", tool.owner.id,
                                       "The shed" + tool.shed.__str__() + " has been deregistered. Your " + tool.name + "'s location has been changed to Home")
            self.send_email_if_notification_enabled('shed_delete',
                                            "The shed" + tool.shed.__str__() + " has been deregistered.",
                                           tool)
        
        for tool in tools:
            tool.shed = None
            tool.save()
        
        
        
        
        
    def get_inclusion_requests(self, user_id):
        try:
            tools = Shed.objects.exclude(active=False).filter(coordinator_id = user_id)[0].tools_requesting.all()
        except IndexError:
            raise Shed.DoesNotExist
        
        return tools
    
    def approve_tool(self, tool_id, user_id):
        tool = Tool.objects.get(id = tool_id)
        
        try:
            shed = Shed.objects.exclude(active=False).filter(coordinator_id = user_id)[0]
        except IndexError:
            raise Shed.DoesNotExist
        
        for reservation in reservationService.get_reservations_by_tool(tool_id):
            reservationService.cancel_lend(reservation.id, reservation.tool.owner_id)        
        
        tool.set_shed(shed.id)
        tool.save()
    
    def reject_tool(self, tool_id):
        tool = Tool.objects.get(id = tool_id)        
        tool.reset_requested_shed()
        tool.save()