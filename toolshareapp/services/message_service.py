from toolshareapp.models import Message

class MessageService:
    
    def create(self, message):
        message.create();
        message.save();
        
    
    def delete(self, message_id):
        message.deactivate()
        message.save()
        
    def get_messages_to_user(self, user_id):
        messages = Message.objects.filter(to_user_id=user_id).order_by('-time')
        return messages;
    
    def get_message(self, message_id):
        return Message.objects.get(id=message_id)