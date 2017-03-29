from django.forms import ModelForm
from django import forms

from toolshareapp.models import Shed

class ShedForm(ModelForm):    
    class Meta:
        
        HOUR_CHOICES = (
            ('AM', (
                ('0:00:00', '12:00 AM'),
                ('1:00:00', '1:00 AM'),
                ('2:00:00', '2:00 AM'),
                ('3:00:00', '3:00 AM'),
                ('4:00:00', '4:00 AM'),
                ('5:00:00', '5:00 AM'),
                ('6:00:00', '6:00 AM'),
                ('7:00:00', '7:00 AM'),
                ('8:00:00', '8:00 AM'),
                ('9:00:00', '9:00 AM'),
                ('10:00:00', '10:00 AM'),
                ('11:00:00', '11:00 AM'))
            ),
            ('PM', (
                ('12:00:00', '12:00 PM'),
                ('13:00:00', '1:00 PM'),
                ('14:00:00', '2:00 PM'),
                ('15:00:00', '3:00 PM'),
                ('16:00:00', '4:00 PM'),
                ('17:00:00', '5:00 PM'),
                ('18:00:00', '6:00 PM'),
                ('19:00:00', '7:00 PM'),
                ('20:00:00', '8:00 PM'),
                ('21:00:00', '9:00 PM'),
                ('22:00:00', '10:00 PM'),
                ('23:00:00', '11:00 PM'))             
            )
        )
        
        model = Shed
        fields = ['house_number', 'street_name', 'open_from', 'open_to']
        widgets = {
            'house_number': forms.TextInput(attrs = { 'required': 'required' }),
            'street_name': forms.TextInput(attrs = { 'required': 'required' }),
            'open_from': forms.Select(choices = HOUR_CHOICES),
            'open_to': forms.Select(choices = HOUR_CHOICES)
        }

