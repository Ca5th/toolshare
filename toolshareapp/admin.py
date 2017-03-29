from django.contrib import admin
from toolshareapp.models import *

admin.site.register(ToolCategory)
admin.site.register(User)
admin.site.register(Shed)
admin.site.register(Tool)
admin.site.register(Reservation)
admin.site.register(ReservationHistory)
admin.site.register(Notification)
admin.site.register(Message)