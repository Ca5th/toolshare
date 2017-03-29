from django.db import models

class ToolCategory(models.Model):
    
    class Meta:
        app_label = 'toolshareapp'
    
    description = models.CharField(max_length = 500)
    
    def __str__(self):
        return self.description