from toolshareapp.models import Reservation
from django.db.models import Count
from django.db.models.query import QuerySet

class StatisticService:
    
    def get_most_active_lenders(self):
        lenders = Reservation.objects.values('tool__owner__name', 'tool__owner__lastname', 'tool__owner__id').\
        annotate(count=Count('tool__owner__name')).order_by('-count')[:5]
        return lenders
    
    def get_most_active_borrowers(self):
        borrowers = Reservation.objects.values('user__name', 'user__lastname', 'user__id').\
        annotate(count=Count('user__name')).order_by('-count')[:5]
        return borrowers
    
    def get_most_used_tools(self):
        tools = Reservation.objects.values('tool__id', 'tool__owner__name', 'tool__owner__lastname', 'tool__name', 'tool__owner__id').\
        annotate(count=Count('tool__id')).order_by('-count')[:5]
        return tools