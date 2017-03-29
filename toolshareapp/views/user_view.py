from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.forms import ModelForm
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from toolshareapp.services import UserService
from toolshareapp.views.forms import UserCreateForm
from toolshareapp.views.forms import UserEditForm
from django.views.decorators.http import require_GET, require_POST
from django import template
from django.http import HttpResponse
from django.utils import simplejson

from toolshareapp.models import User
from toolshareapp.views.errors import error404

from django.db.models import Q

service = UserService()

login_form_url = '/toolshare/login/'

register = template.Library()

class UserView:
    
    @require_GET
    @login_required(login_url=login_form_url)
    def index(request):
        search_term = request.session.get('search_term', None)
        
        context = {
            'users': service.get_users(search_term, request.user.id),
            'search_term': search_term,
            'show_search': True
        }
        
        return render(request, 'toolshareapp/user/index.html', context)
    
    @require_POST
    @login_required(login_url=login_form_url)
    def search(request):
        request.session['search_term'] = request.POST['search_term']
        
        return HttpResponseRedirect(reverse('user.index'))
    
    
    def user_auto_complete(request):
        term = request.GET['term']
        
        users = User.objects.filter(
                Q(name__contains = term) |
                Q(lastname__contains = term) |
                Q(email__contains = term), active=True
                )
        
        users_list = []
   
        for u in users:
             value = '%s, %s (%s)' % (u.lastname, u.name, u.email)
             u_dict = {'id': u.id, 'label': value, 'value': value}
             users_list.append(u_dict)
   
        return HttpResponse(simplejson.dumps(users_list),mimetype='application/json')
    
    @require_GET
    def create(request):
        context = { 'form': UserCreateForm() }
        return render(request, 'toolshareapp/user/create.html', context)
    
    @require_POST
    def create_post(request):
        
        f = UserCreateForm(request.POST, request.FILES)
        
        if f.is_valid():
            new_user = f.get_model() # f.save(commit=False)
            
            try:
                service.register(new_user)
            except IntegrityError:
                messages.error(request, 'The email you specified already exists.')
                return render(request, 'toolshareapp/user/create.html', {'form': f})
                
            user = authenticate(username=new_user.email, password=new_user.password)
            login(request, user)
            
            messages.success(request, 'You are now registered.')
            return HttpResponseRedirect(reverse('tool.index'))
        
        messages.error(request, 'Validation errors occurred.')
        return render(request, 'toolshareapp/user/create.html', {'form': f})
    
    @require_GET
    @login_required(login_url=login_form_url)
    def edit(request): 
        edit_user = service.get_user(request.user.id)
        context = { 'form': UserEditForm(instance=edit_user) }
        return render(request, 'toolshareapp/user/edit.html', context)
    
    @require_POST
    @login_required(login_url=login_form_url)
    def edit_post(request):
        user = service.get_user(request.user.id)
        form = UserEditForm(request.POST, request.FILES, instance=user)        
        if form.is_valid():
           edit_user = form.save(commit = False)
           service.update(edit_user)
           messages.success(request, 'Profile modified sucessfully.')
           return HttpResponseRedirect(reverse('user.edit.get'))
        
        messages.error(request, 'Validation errors occurred.')   
        return render(request, 'toolshareapp/user/edit.html', {'form': form})
    
    @require_GET
    @login_required(login_url=login_form_url)
    def details(request, user_id):
        try:
            context = { 'user' : service.get_user(user_id) }
        except User.DoesNotExist:
            return error404(request)
        
        return render(request, 'toolshareapp/user/details.html', context)
        
    @require_POST
    @login_required(login_url=login_form_url)
    def cancel(request, user_id):
        service.deactivate(user_id)        
        messages.success(request, 'Account cancelled successfully.')
        return HttpResponseRedirect(reverse('user'))
    