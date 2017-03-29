from django.forms import ModelForm
from django.db.models.fields.files import FieldFile
from django.core.validators import *
from django import forms
from toolshareapp.models import ToolCategory
from toolshareapp.models import Tool, Shed, User
from toolshareapp.services import ShedService
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from toolshareapp.views.forms.form_cleaners import clean_picture

class ToolForm(ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(ToolForm, self).__init__(*args, **kwargs) # populates the post
        self.fields['shed'].queryset = ShedService().get_sheds(user_id)
        self.fields['shed'].required = False
        self.fields['shed'].empty_label = 'Home'
        
    class Meta:
        model = Tool
        fields = ['name', 'description', 'picture_url', 'categories', 'shed']
        widgets = {
            'name': forms.TextInput(attrs = { 'required': 'required' }),
            'description': forms.Textarea(attrs = { 'rows': 5, 'cols': 40, 'maxlength': 200, 'required': 'required' }),
            #'picture_url': forms.ClearableFileInput(label = 'Picture'),
            'categories': forms.SelectMultiple(attrs = { 'required': 'required' })
        }
        
    def clean(self):                
        return clean_picture(self, 'picture_url').cleaned_data
