from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from toolshareapp.models import Message, User
from toolshareapp.services import MessageService
from toolshareapp.views.forms import MessageForm
from django.views.decorators.http import require_GET, require_POST

service = MessageService() # Look! Dependency injection in django! lawl!

login_form_url = '/toolshare/login/'

class MessageView:
    
    @require_GET
    @login_required(login_url=login_form_url)
    def index(request):
        private_messages=service.get_messages_to_user(request.user.id)
        
        context = {
            'private_messages': private_messages
        }
        
        return render(request, 'toolshareapp/message/index.html', context)
    
    @require_GET
    @login_required(login_url=login_form_url)
    def create(request):
        context = { 'form': MessageForm() }
        return render(request, 'toolshareapp/message/create.html', context)
    
    @require_POST
    @login_required(login_url=login_form_url)
    def create_post(request):                
        form = MessageForm(request.POST)
        
        if form.is_valid():
            new_message = form.save(commit = False)
            new_message.from_user_id = request.user.id
           
            service.create(new_message)
           
            messages.success(request, 'Message was sent succesfully.')
            return HttpResponseRedirect(reverse('message'))
        
        messages.error(request, 'Validation errors occurred.')                
        return render(request, 'toolshareapp/message/create.html', { 'form': form })
    
    @require_GET
    @login_required(login_url=login_form_url)
    def reply(request, message_id):
        answer_to = service.get_message(message_id)
        context = { 'form': MessageForm(initial = {
                                                   'answer_to': answer_to.id,
                                                   'subject': "RE: " + answer_to.subject,
                                                   'text': "\n\nReply to:\n" + answer_to.from_user.name + ":\n" + answer_to.text,
                                                   'to_user': answer_to.from_user,
                                                   }) }
        return render(request, 'toolshareapp/message/create.html', context)