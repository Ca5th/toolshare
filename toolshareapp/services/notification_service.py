from toolshareapp.models import User, Notification

class NotificationService:
    
    def create(self, link, user_id, text):
        new_notification = Notification.objects.create(link = link, user_id = user_id,
                                                       viewed = False, text = text)
        new_notification.save()
        
    def get_notifications_by_user(self, user_id):
        notifications = Notification.objects.filter(user_id=user_id).order_by('-id')
        return notifications
    
    def user_has_new_notifications(self, user_id):
        return Notification.objects.filter(user_id=user_id).filter(viewed=0).exists()
    
    def mark_as_viewed(self, notification_id):
        notification = Notification.objects.get(id=notification_id)
        notification.viewed = True
        notification.save()
        
    def get_notification(self, notification_id):
        return Notification.objects.get(id=notification_id)

