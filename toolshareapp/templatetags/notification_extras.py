from django import template
from toolshareapp.services import NotificationService

register = template.Library()
service = NotificationService()

@register.inclusion_tag('toolshareapp/notification/notifications.html')
def show_notifications(userId):
    notifications = service.get_notifications_by_user(userId);
    new_notifications = service.user_has_new_notifications(userId);
    return {'notifications': notifications,
            'new_notifications': new_notifications
            }