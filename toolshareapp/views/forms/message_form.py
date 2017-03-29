from django.forms import ModelForm
from toolshareapp.models import Message
from django import forms

class MessageForm(ModelForm):
    
    to_user_display = forms.CharField(max_length=100, help_text='type name or username or email')
    
    class Meta:
        model = Message
        fields = ['to_user','to_user_display','subject','text','answer_to']
        widgets = {
            'answer_to': forms.HiddenInput(),
            'to_user': forms.HiddenInput()
        }
        
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['answer_to'].required = False
        self.fields['to_user_display'].label = "Add a user"
            
    
    
    