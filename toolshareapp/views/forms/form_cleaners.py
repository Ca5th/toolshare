from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.fields.files import FieldFile
from django import forms

def clean_picture(form_to_clean, picture_field_name):
    if picture_field_name in form_to_clean.cleaned_data:
        content = form_to_clean.cleaned_data[picture_field_name]
        
        if type(content) != FieldFile:            
            content_type = content.content_type.split('/')[0]
            
            if content_type in settings.CONTENT_TYPES:
                if content._size > settings.MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
            else:
                raise forms.ValidationError(_('File type is not supported'))
        
    return form_to_clean