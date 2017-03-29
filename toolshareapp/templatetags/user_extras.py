from django import template
from toolshareapp.services import UserService

register = template.Library()
service = UserService()

@register.inclusion_tag('toolshareapp/user/owned_shed_navigation.html')
def has_shed(user_id):
    user_has_shed = service.has_shed(user_id);
    
    return { 'user_has_shed': user_has_shed }