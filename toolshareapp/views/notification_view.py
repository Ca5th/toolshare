from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from  django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from toolshareapp.services import NotificationService
from toolshareapp.models import Notification
from django.views.decorators.http import require_GET, require_POST
from toolshareapp.views.errors import error404

service = NotificationService()

login_form_url = '/toolshare/login/'

class NotificationView:
    
    @require_GET
    @login_required(login_url=login_form_url)
    def index(request):
        context = {
            'notifications': service.get_notifications_by_user(request.user.id)
        }
        
        return render(request, 'toolshareapp/notification/index.html', context,
                      context_instance=RequestContext(request))
    
    @require_POST
    def mark_as_viewed(request, notification_id):
        try:
            service.mark_as_viewed(notification_id)
        except Notification.DoesNotExist:
            return error404(request)
        
        notification = service.get_notification(notification_id)
        return HttpResponseRedirect(notification.link)      