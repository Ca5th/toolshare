from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from toolshareapp.services import StatisticService

from django.views.decorators.http import require_GET, require_POST

from toolshareapp.views.errors import error404

service = StatisticService()

login_form_url = '/toolshare/login/'

class StatisticView:
    
    @require_GET
    @login_required(login_url=login_form_url)
    def index(request):   
        context = {
            'most_active_lenders': service.get_most_active_lenders(),
            'most_active_borrowers': service.get_most_active_borrowers(),
            'most_used_tools': service.get_most_used_tools(),
            
        }   
        
        return render(request, 'toolshareapp/statistic/index.html', context)
    