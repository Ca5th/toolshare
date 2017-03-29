from django.forms import ModelForm
from django.db.models.fields.files import FieldFile
from django.core.validators import *
from toolshareapp.models import User
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from toolshareapp.views.forms.form_cleaners import clean_picture

class UserCreateForm(forms.Form):
    email = forms.CharField(validators = [validate_email],
                            widget = forms.TextInput(attrs = { 'required': 'required' }))
    name = forms.CharField(validators = [MaxLengthValidator(50)],
                           widget = forms.TextInput(attrs = { 'required': 'required' }))
    lastname = forms.CharField(validators = [MaxLengthValidator(50)],
                               widget = forms.TextInput(attrs = { 'required': 'required' }))
    password = forms.CharField(widget = forms.PasswordInput(attrs = { 'required': 'required' }),
                               validators = [MaxLengthValidator(500)])
    password_confirmation = forms.CharField(widget = forms.PasswordInput(attrs = { 'required': 'required' }),
                                            validators = [MaxLengthValidator(500)])
    picture = forms.FileField()
    house_number = forms.CharField(validators = [MaxLengthValidator(5)],
                                   widget = forms.TextInput(attrs = { 'required': 'required' }))
    street_name = forms.CharField(validators= [MaxLengthValidator(500)],
                                  widget = forms.TextInput(attrs = { 'required': 'required' }))
    zip_code = forms.CharField(validators = [MinLengthValidator(5), MaxLengthValidator(5),
                                             RegexValidator(regex = r'^[0-9]+$')],
                               widget = forms.TextInput(attrs = { 'required': 'required', 'maxlength': 5 }))
    phone_number = forms.CharField(validators = [MaxLengthValidator(10),
                                                 MinLengthValidator(10),
                                                 RegexValidator(regex = r'^[0-9]+$')],
                                   widget = forms.TextInput(attrs = { 'required': 'required', 'maxlength': 10 }))
    preferred_pickup_location = forms.CharField(widget = forms.Textarea(attrs = { 'rows': 5, 'cols': 40, 'required': 'required' }),
                                                validators=[MaxLengthValidator(500)])
    email_notifications = forms.BooleanField(required = False)
    preferred_contact_method = forms.CharField(validators = [MaxLengthValidator(500)],
                                               widget = forms.TextInput(attrs = { 'required': 'required' }))

    def get_model(self):
        return User(email = self.cleaned_data['email'],
                    name = self.cleaned_data['name'],
                    lastname = self.cleaned_data['lastname'],
                    password = self.cleaned_data['password'],
                    house_number = self.cleaned_data['house_number'],
                    street_name = self.cleaned_data['street_name'],
                    zip_code = self.cleaned_data['zip_code'],
                    phone_number = self.cleaned_data['phone_number'],
                    preferred_pickup_location = self.cleaned_data['preferred_pickup_location'],
                    email_notifications = self.cleaned_data['email_notifications'],
                    preferred_contact_method = self.cleaned_data['preferred_contact_method'],
                    picture = self.cleaned_data['picture'])
    
    def clean(self):        
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirmation')
    
        if password1 and password1 != password2:
            raise forms.ValidationError("The passwords must match")
        
        return clean_picture(self, 'picture').cleaned_data

class UserEditForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['name', 'lastname', 'picture', 'house_number', 'street_name', 'zip_code', 'phone_number',
                  'preferred_pickup_location', 'email_notifications', 'preferred_contact_method']
        widgets = {
            'name': forms.TextInput(attrs = { 'required': 'required' }),
            'lastname': forms.TextInput(attrs = { 'required': 'required' }),
            'house_number': forms.TextInput(attrs = { 'required': 'required' }),
            'street_name': forms.TextInput(attrs = { 'required': 'required' }),
            'zip_code': forms.TextInput(attrs = { 'required': 'required' }),
            'phone_number': forms.TextInput(attrs = { 'required': 'required' }),
            'preferred_pickup_location': forms.Textarea(attrs = { 'rows': 5, 'cols': 40, 'required': 'required' }),
            'preferred_contact_method': forms.TextInput(attrs = { 'required': 'required' })
        }
    
    def clean(self):
        return clean_picture(self, 'picture').cleaned_data
