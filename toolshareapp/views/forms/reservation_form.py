from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets 
from django.db.models import Q
import datetime

from toolshareapp.models import Reservation
from toolshareapp.models import ReservationStatus

class RejectionForm(forms.Form):
    reason = forms.CharField(max_length = 200,
                             required = True,
                             widget = forms.TextInput(attrs = { 'required': 'required' }))
    
    def get_reason(self):
        return self.cleaned_data['reason']

class ApprovalForm(forms.Form):
    pickup = forms.CharField(max_length = 200,
                             required = True,
                             widget = forms.TextInput(attrs = { 'required': 'required' }))
    
    def get_pickup(self):
        return self.cleaned_data['pickup']

class ReservationForm(forms.Form):
    start_date = forms.DateField(widget = forms.TextInput(attrs = {
        'class': 'datepicker', 'required': 'required'
    }))
    end_date = forms.DateField(widget = forms.TextInput(attrs = {
        'class': 'datepicker', 'required': 'required'
    }))
    comment = forms.CharField(required = False,
                              max_length = 200,
                              widget = forms.Textarea(attrs = {
                                'rows': 5, 'cols': 40, 'maxlength': 200
                              }))
    requested_tool_id = forms.IntegerField(widget = forms.HiddenInput)
    
    def get_model(self):
        return Reservation(start_date = self.cleaned_data['start_date'],
                           end_date = self.cleaned_data['end_date'],
                           comment = self.cleaned_data['comment'],
                           tool_id = self.cleaned_data['requested_tool_id'])
    
    def clean(self):
        super(forms.Form,self).clean()
        reservations_for_tool = Reservation.objects.filter(
            tool__id=self.cleaned_data['requested_tool_id']).filter(
            Q(status=ReservationStatus.Awating_for_start_date) | Q(status=ReservationStatus.Pending_approval))
        
        if 'start_date' in self.cleaned_data and 'end_date' in self.cleaned_data:
            if self.cleaned_data['start_date'] < datetime.datetime.now().date():
                self._errors['start_date'] = ['Start date must not be in the past.']
                
            if self.cleaned_data['end_date'] < datetime.datetime.now().date():
                self._errors['end_date'] = ['End date must not be in the past.']
                
            if self.cleaned_data['start_date'] > self.cleaned_data['end_date']:
                self._errors['start_date'] = ['Start date has to be earlier.']
                self._errors['end_date'] = ['Start date has to be earlier.']
                
            if reservations_for_tool.filter(start_date__gte=self.cleaned_data['start_date']).filter(start_date__lte=self.cleaned_data['end_date']).exists():
                self._errors['start_date'] = ['This tool is already reserved for this date']
                
            if reservations_for_tool.filter(end_date__gte=self.cleaned_data['start_date']).filter(end_date__lte=self.cleaned_data['end_date']).exists():
                self._errors['end_date'] = ['This tool is already reserved for this date']
                
            if reservations_for_tool.filter(start_date__lte=self.cleaned_data['start_date']).filter(end_date__gte=self.cleaned_data['start_date']).exists():
                self._errors['start_date'] = ['This tool is already reserved for this date']
                
            if reservations_for_tool.filter(start_date__lte=self.cleaned_data['end_date']).filter(end_date__gte=self.cleaned_data['end_date']).exists():
                self._errors['start_date'] = ['This tool is already reserved for this date']
            
            if self.cleaned_data['end_date'] > self.cleaned_data['start_date'] + datetime.timedelta(days=7):
                self._errors['end_date'] = ['End date must not be more than 7 days later than start date']
                
        return self.cleaned_data