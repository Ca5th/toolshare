from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from time import strftime

from toolshareapp.services import ReservationService, UserService
from toolshareapp.views.forms import ReservationForm, RejectionForm, ApprovalForm
from toolshareapp.models import ReservationStatus
from toolshareapp.models import Reservation
from toolshareapp.models import Tool
from django.views.decorators.http import require_GET, require_POST
import datetime

from toolshareapp.views.errors import error404

service = ReservationService()
userService = UserService()

login_form_url = '/toolshare/login/'

def render_incoming(request, rejection_form, approval_form):
    
    approval_form.initial = { 'pickup': userService.get_preferred_pickup_location(request.user.id) }
    
    context = {
        'reservations': service.get_reservations_by_owner(request.user.id),
        
        'rejection_form': rejection_form,
        'approval_form': approval_form,
        
        'awating_for_start_date': ReservationStatus.Awating_for_start_date,
        'ongoing': ReservationStatus.Ongoing,
        'pending_approval': ReservationStatus.Pending_approval,
        'pending_return_acknowledge': ReservationStatus.Pending_return_acknowledge
    }
    
    return render(request, 'toolshareapp/reservation/incoming.html', context)

def render_detail(request, reservation_id, rejection_form, approval_form):
    
    approval_form.initial = { 'pickup': userService.get_preferred_pickup_location(request.user.id) }
    
    try:        
        context = {
            'reservation': service.get_reservation(reservation_id),
            
            'rejection_form': rejection_form,
            'approval_form': approval_form,
            
            'pending_approval': ReservationStatus.Pending_approval,
            'awating_for_start_date': ReservationStatus.Awating_for_start_date,
            'ongoing': ReservationStatus.Ongoing,
            'pending_return': ReservationStatus.Pending_return,
            'pending_return_acknowledge': ReservationStatus.Pending_return_acknowledge,
            'reservationhistory_set': service.get_reservation_history(reservation_id)
        }            
    except Reservation.DoesNotExist:
        return error404(request)
    
    return render(request, 'toolshareapp/reservation/detail.html', context)

def render_create(request, tool_id, title):
    unavailable_dates_str = format_as_string_array(*service.get_reserved_dates_for_tool(tool_id))
    
    context = { 'form': ReservationForm(initial = { 'requested_tool_id': tool_id }),
                'title': title,
                'unavailable_dates_str':unavailable_dates_str }
    return render(request, 'toolshareapp/reservation/create.html', context)

def format_as_string_array(dates_start, dates_end):
    
    dates_str = []
    
    for start, end in zip(dates_start, dates_end):
        numdays = (end - start).days
        dates_str.extend([ str(start + datetime.timedelta(days=x)) for x in range(0,numdays+1) ])

    return dates_str

class ReservationView:
    
    @require_GET
    @login_required(login_url=login_form_url)
    def index(request):
        
        context = {
            'reservations': service.get_reservations_by_user(request.user.id),
            
            'pending_approval': ReservationStatus.Pending_approval,
            'awating_for_start_date': ReservationStatus.Awating_for_start_date,
            'ongoing': ReservationStatus.Ongoing,
            'pending_return': ReservationStatus.Pending_return
        }
        
        return render(request, 'toolshareapp/reservation/index.html', context)
    
    @require_GET
    @login_required(login_url=login_form_url)
    def detail(request, reservation_id):
        return render_detail(request, reservation_id, RejectionForm(), ApprovalForm()) 
    
    @require_POST
    @login_required(login_url=login_form_url)
    def detail_approve(request, reservation_id):
        form = ApprovalForm(request.POST)
        
        if form.is_valid():
            try:
                service.approve_borrower(reservation_id, request.user.id, form.get_pickup())
            except Reservation.DoesNotExist:
                return error404(request)
            
            messages.success(request, 'Reservation approved.')
            return HttpResponseRedirect(reverse('reservation.detail.get', kwargs = { 'reservation_id': reservation_id }))
        
        messages.error(request, 'Validation errors occured.')
        return render_detail(request, reservation_id, RejectionForm(), form)
    
    @require_POST
    @login_required(login_url=login_form_url)
    def detail_reject(request, reservation_id):
        form = RejectionForm(request.POST)
        
        if form.is_valid():
            try:
                service.reject_borrower(reservation_id, request.user.id, form.get_reason())
            except Reservation.DoesNotExist:
                return error404(request)
            
            messages.success(request, 'Reservation rejected.')
            return HttpResponseRedirect(reverse('reservation.detail.get', kwargs = { 'reservation_id': reservation_id }))
        
        messages.error(request, 'Validation errors occured.')
        return render_detail(request, reservation_id, form, ApprovalForm())
    
    @require_GET
    @login_required(login_url=login_form_url)
    def incoming(request):
        return render_incoming(request, RejectionForm(), ApprovalForm())

    @require_GET
    @login_required(login_url=login_form_url)
    def create(request, tool_id):
        return render_create(request, tool_id, "Request tool")
    
    @require_GET
    @login_required(login_url=login_form_url)
    def change_availability(request, tool_id):
        return render_create(request, tool_id, "Change tool availability")

    @require_POST
    @login_required(login_url=login_form_url)
    def create_post(request):
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            new_reservation = form.get_model()
            new_reservation.user_id = request.user.id
            
            try:
                service.request_borrow(new_reservation, request.user.id)
            except Tool.DoesNotExist:
                return error404(request)

            messages.success(request, 'Reservation was created successfully.')
            return HttpResponseRedirect(reverse('reservation'))
        
        unavailable_dates_str = format_as_string_array(*service.get_reserved_dates_for_tool(form.data['requested_tool_id']))
            
        messages.error(request, 'Validation errors occured.')
        
        if 'changeAvailability' in request.META['HTTP_REFERER']:
            title = "Change tool availability"
        else:
            title = "Request tool"
        
        return render(request, 'toolshareapp/reservation/create.html', {'form': form,
                                                                        'title': title,
                                                                        'unavailable_dates_str':unavailable_dates_str})
    
    @require_POST
    @login_required(login_url=login_form_url)
    def cancel_lend(request, reservation_id):
        try:
            service.cancel_lend(reservation_id, request.user.id)
        except Reservation.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Reservation cancelled.')
        return HttpResponseRedirect(reverse('reservation.incoming'))
    
    @require_POST
    @login_required(login_url=login_form_url)
    def cancel_borrow(request, reservation_id):
        try:
            service.cancel_borrow(reservation_id, request.user.id)
        except Reservation.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Reservation cancelled.')
        return HttpResponseRedirect(reverse('reservation'))
    
    @require_POST
    @login_required(login_url=login_form_url)
    def approve(request, reservation_id):
        
        form = ApprovalForm(request.POST)
        
        if form.is_valid():
            try:
                service.approve_borrower(reservation_id, request.user.id, form.get_pickup())
            except Reservation.DoesNotExist:
                return error404(request)
            
            messages.success(request, 'Reservation approved.')
            return HttpResponseRedirect(reverse('reservation.incoming'))
        
        messages.error(request, 'Validation errors occured.')
        return render_incoming(request, RejectionForm(), form)
    
    @require_POST
    @login_required(login_url=login_form_url)
    def reject(request, reservation_id):
        #rejection_reason = request.POST['rejection_reason']
        form = RejectionForm(request.POST)
        
        if form.is_valid():        
            try:
                service.reject_borrower(reservation_id, request.user.id, form.get_reason())
            except Reservation.DoesNotExist:
                return error404(request)
            
            messages.success(request, 'Reservation rejected.')
            return HttpResponseRedirect(reverse('reservation.incoming'))
        
        messages.error(request, 'Validation errors occured.')
        return render_incoming(request, form, ApprovalForm())
    
    @require_POST
    @login_required(login_url=login_form_url)
    def return_tool(request, reservation_id):
        try:        
            service.return_tool(reservation_id, request.user.id)
        except Reservation.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Tool returned.')
        return HttpResponseRedirect(reverse('reservation'))    
    
    @require_POST
    @login_required(login_url=login_form_url)
    def acknowledge_return(request, reservation_id):
        try:
            service.acknowledge_tool_return(reservation_id, request.user.id)
        except Reservation.DoesNotExist:
            return error404(request)
        
        messages.success(request, 'Tool return acknowledged.')
        return HttpResponseRedirect(reverse('reservation.incoming'))