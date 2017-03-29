from django.db import models

from toolshareapp.models.shed import Shed
from toolshareapp.models.tool_status import ToolStatus
from toolshareapp.models.user import User
from toolshareapp.models.tool_category import ToolCategory

class Tool(models.Model):
    
    class Meta:
        app_label = 'toolshareapp'
    
    name = models.CharField(max_length = 100)
    description = models.TextField(max_length = 200)
    #picture_url = models.CharField(max_length = 500)
    picture_url = models.FileField(upload_to = 'tool')
    active = models.BooleanField()
    
    shed = models.ForeignKey(Shed, null = True)
    requested_shed = models.ForeignKey(Shed, null = True, related_name='tools_requesting')
    status = models.CharField(max_length=100)
    owner = models.ForeignKey(User)
    categories = models.ManyToManyField(ToolCategory)
    
    def __str__(self):
        return self.name
    
    def deactivate(self):
        self.active = False
        
    def make_unavailable(self):
        self.status = ToolStatus.Unavailable
    
    def make_available(self):
        self.status = ToolStatus.Available
        
    def set_shed(self, shed_id):
        self.shed_id = shed_id
        self.requested_shed = None
    
    def reset_requested_shed(self):
        self.requested_shed = None