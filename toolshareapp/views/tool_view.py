from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from toolshareapp.models import ToolStatus
from toolshareapp.models import Tool
from toolshareapp.services import ToolService, ToolHasReservationsError
from toolshareapp.views.forms import ToolForm
from django.views.decorators.http import require_GET, require_POST

from toolshareapp.views.errors import error404

service = ToolService() # Look! Dependency injection in django! lawl!

login_form_url = '/toolshare/login/'

class ToolView:    
    
    @require_GET
    @login_required(login_url=login_form_url)
    def index(request):
        search_term = request.session.get('search_term', None)        

        context = {
            'tools': service.get_tools(search_term, request.user.id),
            'search_term': search_term,
            
            'available': ToolStatus.Available,
            'unavailable': ToolStatus.Unavailable,
            
            'show_search': True
        }   
        
        return render(request, 'toolshareapp/tool/index.html', context)
    
    @require_GET
    @login_required(login_url=login_form_url)
    def owned(request):
        context = {
            'tools': service.get_tools_owned_by_user(request.user.id),
                   
            'available': ToolStatus.Available,
            'unavailable': ToolStatus.Unavailable,
            
            'show_search': True
        }
        
        return render(request, 'toolshareapp/tool/index.html', context)
    
    @require_GET
    @login_required(login_url=login_form_url)
    def shed(request):
        search_term = request.session.get('search_term', None)
        
        context = {
            'tools': service.get_tools_in_users_shed(search_term, request.user.id),
                   
            'available': ToolStatus.Available,
            'unavailable': ToolStatus.Unavailable,
            
            'search_term': search_term,
            'show_search': True,
            'search_in': 'Shed'
        }
        
        return render(request, 'toolshareapp/tool/index.html', context)
    
    @require_POST
    @login_required(login_url=login_form_url)
    def search(request):
        request.session['search_term'] = request.POST['search_term']
        
        if request.POST['search_in'].strip() == 'Shed':
            return HttpResponseRedirect(reverse('tool.shed'))
        else: 
            return HttpResponseRedirect(reverse('tool.index'))    
    
    @require_GET
    @login_required(login_url=login_form_url)
    def create(request):
        context = { 'form': ToolForm(request.user.id) }        
        return render(request, 'toolshareapp/tool/create.html', context)
    
    @require_POST
    @login_required(login_url=login_form_url)
    def create_post(request):                
        form = ToolForm(request.user.id, request.POST, request.FILES)
        
        if form.is_valid():
            new_tool = form.save(commit = False)
            new_tool.owner_id = request.user.id
            
            service.register(new_tool)
            form.save_m2m()
           
            messages.success(request, 'Tool created succesfully.')
            return HttpResponseRedirect(reverse('tool.owned'))
        
        messages.error(request, 'Validation errors occurred.')                
        return render(request, 'toolshareapp/tool/create.html', { 'form': form })        
    
    @require_GET
    @login_required(login_url=login_form_url)    
    def edit(request, tool_id):
        try:
            edit_tool = service.get_tool(tool_id)
        except Tool.DoesNotExist:
            return error404(request)
        
        context = { 'form': ToolForm(request.user.id, instance = edit_tool), 'tool_id': tool_id }
        return render(request, 'toolshareapp/tool/edit.html', context)
    
    @require_POST
    @login_required(login_url=login_form_url)    
    def edit_post(request, tool_id):
        try:
            tool = service.get_tool(tool_id)
            
            form = ToolForm(request.user.id, request.POST , request.FILES, instance = tool)
            
            if form.is_valid():
               edit_tool = form.save(commit = False)           
               service.update(edit_tool, request.user.id)
               form.save_m2m() # TODO: implement this in ToolService.register()
               messages.success(request, 'Tool updated succesfully.')
               return HttpResponseRedirect(reverse('tool.edit.get', kwargs = { 'tool_id': tool_id }))
            else:
                messages.error(request, 'Validation errors occurred.')
            
        except Tool.DoesNotExist:
            return error404(request)
        
        except ToolHasReservationsError as e:
            messages.error(request, e.msg)
            
        return render(request, 'toolshareapp/tool/edit.html', {'form': form, 'tool_id': tool_id})
    
    @require_POST
    @login_required(login_url=login_form_url)
    def deregister(request, tool_id):
        try:
            service.deregister(tool_id)        
        except Tool.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Tool deregistered succesfully.')
        return HttpResponseRedirect(reverse('tool.owned'))
    
    @require_POST
    @login_required(login_url=login_form_url)
    def withhold(request, tool_id):
        try:
            service.withhold(tool_id)
        except Tool.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Tool withheld succesfully.')
        return HttpResponseRedirect(reverse('tool.owned'))
    
    @require_POST
    @login_required(login_url=login_form_url)
    def release(request, tool_id):
        try:
            service.release(tool_id)
        except Tool.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Tool released succesfully.')
        return HttpResponseRedirect(reverse('tool.owned'))