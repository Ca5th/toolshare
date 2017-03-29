from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from toolshare import settings
from toolshareapp import views
#from ajax_select import urls as ajax_select_urls

import os, django
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath('__file__'))

#from django.conf import settings

urlpatterns = patterns('',
    
    #url(r'^admin/lookups/', include(ajax_select_urls)),
    #url(r'^admin/', include(admin.site.urls)),
    
    # /toolshare/
    url(r'^$', views.ToolView.index, name='index'),
    
    url(r'^user/user_auto_complete/$', views.UserView.user_auto_complete, name='user.user_auto_complete'),
    
    # GET /toolshare/statistic/ 
    url(r'^statistic/$', views.StatisticView.index, name='statistic'),
    # GET /toolshare/statistic/index/
    url(r'^statistic/index/$', views.StatisticView.index, name='statistic.index'),
    
    # GET /toolshare/tool/ 
    url(r'^tool/$', views.ToolView.index, name='tool'),
    # GET /toolshare/tool/index/
    url(r'^tool/index/$', views.ToolView.index, name='tool.index'),
    # GET /toolshare/tool/index/owned
    url(r'^tool/owned/$', views.ToolView.owned, name='tool.owned'),
    # GET /toolshare/tool/index/shed
    url(r'^tool/shed/$', views.ToolView.shed, name='tool.shed'),
    # POST /toolshare/tool/search/
    url(r'tool/search/$', views.ToolView.search, name='tool.search.post'),
    # GET /toolshare/tool/create/
    url(r'^tool/create/$', views.ToolView.create, name='tool.create.get'),
    # POST /toolshare/tool/create/post/
    url(r'^tool/create/post/$', views.ToolView.create_post, name='tool.create.post'),
    # GET /toolshare/tool/edit/1
    url(r'^tool/edit/(?P<tool_id>\d+)/$', views.ToolView.edit, name='tool.edit.get'),
    # POST /toolshare/tool/edit/post/1
    url(r'^tool/edit/post/(?P<tool_id>\d+)/$', views.ToolView.edit_post, name='tool.edit.post'),
    # POST /toolshare/tool/deregister/1
    url(r'^tool/deregister/(?P<tool_id>\d+)/$', views.ToolView.deregister, name='tool.deregister.post'),
    # POST /toolshare/tool/withhold/1
    url(r'^tool/withhold/(?P<tool_id>\d+)/$', views.ToolView.withhold, name='tool.withhold.post'),
    # POST /toolshare/tool/release/1
    url(r'^tool/release/(?P<tool_id>\d+)/$', views.ToolView.release, name='tool.release.post'),
    
    # GET /toolshare/message/
    url(r'^message/$', views.MessageView.index, name='message'),
    # GET /toolshare/message/create/
    url(r'^message/create/$', views.MessageView.create, name='message.create.get'),
    # GET /toolshare/message/create/
    url(r'^message/create/post/$', views.MessageView.create_post, name='message.create.post'),
    # GET /toolshare/message/reply/1
    url(r'^message/reply/(?P<message_id>\d+)/$', views.MessageView.reply, name='message.reply.get'),
    
    # GET /toolshare/notification/
    url(r'^notification/$', views.NotificationView.index, name='notification'),
    # POST /toolshare/notification/viewed/1
    url(r'^notification/viewed/(?P<notification_id>\d+)/$', views.NotificationView.mark_as_viewed, name='notification.mark_as_viewed.post'),
    
    # GET /toolshare/reservation/
    url(r'^reservation/$', views.ReservationView.index, name='reservation'),
    # GET /toolshare/reservation/index/
    url(r'^reservation/index/$', views.ReservationView.index, name='reservation.index'),
    # GET /toolshare/reservation/incoming/
    url(r'^reservation/incoming/$', views.ReservationView.incoming, name='reservation.incoming'),
    # GET /toolshare/reservation/changeAvailability/1
    url(r'^reservation/changeAvailability/(?P<tool_id>\d+)/$', views.ReservationView.change_availability, name='reservation.change_availability.get'),
    # GET /toolshare/reservation/create/1
    url(r'^reservation/create/(?P<tool_id>\d+)/$', views.ReservationView.create, name='reservation.create.get'),
    # POST /toolshare/reservation/create/post/
    url(r'^reservation/create/post/$', views.ReservationView.create_post, name='reservation.create.post'),
    # GET /toolshare/reservation/detail/1
    url(r'^reservation/detail/(?P<reservation_id>\d+)/$', views.ReservationView.detail, name='reservation.detail.get'),
    # POST /toolshare/reservation/detail/approve/1
    url(r'^reservation/detail/approve/(?P<reservation_id>\d+)/$', views.ReservationView.detail_approve, name='reservation.detail.approve.post'),
    # POST /toolshare/reservation/detail/reject/1
    url(r'^reservation/detail/reject/(?P<reservation_id>\d+)/$', views.ReservationView.detail_reject, name='reservation.detail.reject.post'),
    # POST /toolshare/reservation/cancel_lend/1
    url(r'^reservation/cancel_lend/(?P<reservation_id>\d+)/$', views.ReservationView.cancel_lend, name='reservation.cancel_lend.post'),
    # POST /toolshare/reservation/cancel_borrow/1
    url(r'^reservation/cancel_borrow/(?P<reservation_id>\d+)/$', views.ReservationView.cancel_borrow, name='reservation.cancel_borrow.post'),
    # POST /toolshare/reservation/approve/1
    url(r'^reservation/approve/(?P<reservation_id>\d+)/$', views.ReservationView.approve, name='reservation.approve.post'),
    # POST /toolshare/reservation/reject/1
    url(r'^reservation/reject/(?P<reservation_id>\d+)/$', views.ReservationView.reject, name='reservation.reject.post'),
    # POST /toolshare/reservation/return_tool/1
    url(r'^reservation/return_tool/(?P<reservation_id>\d+)/$', views.ReservationView.return_tool, name='reservation.return_tool.post'),
    # POST /toolshare/reservation/acknowledge_return/1
    url(r'^reservation/acknowledge_return/(?P<reservation_id>\d+)/$', views.ReservationView.acknowledge_return, name='reservation.acknowledge_return.post'),
    
    # POST /toolshare/user/search
    url(r'^user/search/$', views.UserView.search, name='user.search.post'),
    # GET /toolshare/user/
    url(r'^user/$', views.UserView.index, name='user'),
    # GET /toolshare/user/index/
    url(r'^user/index/$', views.UserView.index, name='user.index'),
    #/toolshare/user/create
    url(r'^user/create/$', views.UserView.create, name='user.create.get'),
    url(r'^user/create/post/$', views.UserView.create_post, name='user.create.post'),    
    #/toolshare/user/edit/  
    url(r'^user/edit/$', views.UserView.edit, name='user.edit.get'),
    #/toolshare/user/edit/post
    url(r'^user/edit/post/$', views.UserView.edit_post, name='user.edit.post'),
    # GET /toolshare/user/details/1
    url(r'^user/details/(?P<user_id>\d+)/$', views.UserView.details, name='user.details'),
    
    # GET /toolshare/shed/ 
    url(r'^shed/$', views.ShedView.index, name='shed'),
    # GET /toolshare/shed/create/
    url(r'^shed/create/$', views.ShedView.create, name='shed.create.get'),
    # POST /toolshare/shed/create/post/
    url(r'^shed/create/post/$', views.ShedView.create_post, name='shed.create.post'),
    # POST /toolshare/shed/deregister/1
    url(r'^shed/deregister/(?P<shed_id>\d+)/$', views.ShedView.deregister, name='shed.deregister.post'),
    # POST /toolshare/shed/deregister/
    url(r'^shed/deregister/', views.ShedView.deregister, name='shed.deregister.mine.post'),
    # GET /toolshare/shed/edit/1
    url(r'^shed/edit/(?P<shed_id>\d+)/$', views.ShedView.edit, name='shed.edit.get'),
    # POST /toolshare/shed/edit/post/1
    url(r'^shed/edit/post/(?P<shed_id>\d+)/$', views.ShedView.edit_post, name='shed.edit.post'),
    # GET /toolshare/shed/requests/
    url(r'^shed/requests/$', views.ShedView.requests, name='shed.requests'),
    # POST /toolshare/shed/approve/1
    url(r'^shed/approve/(?P<tool_id>\d+)/$', views.ShedView.approve_tool, name='shed.approve_tool.post'),
    # POST /toolshare/shed/reject/1
    url(r'^shed/reject/(?P<tool_id>\d+)/$', views.ShedView.reject_tool, name='shed.reject_tool.post'),

url(r'^user/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'template_name': 'toolshareapp/password_reset_form.html'},
        name="password.reset"),

    (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'toolshareapp/password_reset_done.html'}),
    
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'template_name': 'toolshareapp/password_reset_confirm.html'}),
    
    (r'^user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'toolshareapp/password_reset_complete.html'}),
    
    url(r'^login/$', 'django.contrib.auth.views.login',
     { 'template_name': 'toolshareapp/login.html'},
     name="user.login"),
    
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'toolshareapp/logged_out.html'}),
    
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT#cath_lab.MEDIA_ROOT#cath_lab.MEDIA_ROOT,#cath.MEDIA_ROOT #
    })
   
)
