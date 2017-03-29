from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST

from toolshareapp.models import Shed, Tool
from toolshareapp.services import ShedService
from toolshareapp.views.forms import ShedForm
from toolshareapp.views.errors import error404

service = ShedService()

login_form_url = '/toolshare/login/'

class ShedView:    
    
    @require_GET
    @login_required(login_url=login_form_url)
    def index(request):    
        context = { 'sheds': service.get_sheds(request.user.id) }
        
        return render(request, 'toolshareapp/shed/index.html', context)
    
    @require_GET
    @login_required(login_url=login_form_url)    
    def requests(request):
        try:
            context = { 'tools': service.get_inclusion_requests(request.user.id) }
        except Shed.DoesNotExist:
            return error404(request)
        
        return render(request, 'toolshareapp/shed/requests.html', context)
    
    @require_GET
    @login_required(login_url=login_form_url)
    def create(request):
        context = { 'form': ShedForm() }        
        return render(request, 'toolshareapp/shed/create.html', context)
    
    @require_POST
    @login_required(login_url=login_form_url)
    def create_post(request):
        form = ShedForm(request.POST)
        
        if form.is_valid():
            new_shed = form.save(commit = False)
            new_shed.coordinator_id = request.user.id
            
            service.register(new_shed)
            
            messages.success(request, 'Shed created successfully.')
            return HttpResponseRedirect(reverse('shed'))
        
        messages.error(request, 'Validation errors occurred.')
        return render(request, 'toolshareapp/shed/create.html', { 'form': form })
    
    @require_GET
    @login_required(login_url=login_form_url)
    def edit(request, shed_id):
        try:
            edit_shed = service.get_shed(shed_id)
        except Shed.DoesNotExist:
            return error404(request)
            
        context = {'form': ShedForm(instance=edit_shed), 'shed_id': shed_id }
        return render(request, 'toolshareapp/shed/edit.html', context)    
    
    @require_POST
    @login_required(login_url=login_form_url)
    def edit_post(request, shed_id):
        try:
            shed = service.get_shed(shed_id);
        except Shed.DoesNotExist:
            return error404(request)
        
        form = ShedForm(request.POST, instance=shed)
        
        if form.is_valid():
            edit_shed = form.save(commit=False)
            service.update(edit_shed)
            messages.success(request, 'Shed updated successfully.')
            return HttpResponseRedirect(reverse('shed.edit.get', kwargs = { 'shed_id': shed_id }))
        
        messages.error(request, 'Validation errors occurred.')
        render(reques, 'toolshareapp/shed/edit.html', { 'form':form, 'shed_id': shed_id })
        
  
    @login_required(login_url=login_form_url)
    def deregister(request, shed_id=None):
        try:
            if shed_id == None:
                shed_id = service.get_shed_by_user(request.user.id).id
            service.deregister(shed_id)
        except Shed.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Shed deregistered succesfully.')
        return HttpResponseRedirect(reverse('shed'))
    
    @require_POST
    @login_required(login_url=login_form_url)
    def approve_tool(request, tool_id):
        try:
            service.approve_tool(tool_id, request.user.id)
        except (Shed.DoesNotExist, Tool.DoesNotExist):
            return error404(request)
        
        messages.success(request, 'Tool has been moved to the shed.')
        return HttpResponseRedirect(reverse('shed.requests'))
    
    @require_POST
    @login_required(login_url=login_form_url)
    def reject_tool(request, tool_id):
        try:
            service.reject_tool(tool_id)
        except Tool.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Tool has been rejected.')
        return HttpResponseRedirect(reverse('shed.requests'))
    