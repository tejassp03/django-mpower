from . import views
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'employer'

urlpatterns = [
	path('', views.dashboard, name='cdashboard'),
	path('inbox_count/', views.inbox_count, name='inbox_count'),
	path('newjob/', views.newjob, name='newjob'),
	path('edit_profile/', views.edit, name='cedit'),
    path('get_ot/', views.get_ot, name='get_ot'),
    path('post_ot/', views.post_ot, name='post_ot'),
    path('cupd_phone/', views.cupd_phone, name='cupd_phone'),
	path('manage_job/', views.manage, name='manage'),
	path('candidates/', views.candidates, name='candidates'),
	path('subscriptions/', views.subscriptions, name='subscriptions'),
	path('change_pass/', views.change_pass, name='change_pass'),
	path('cinbox/', views.cinbox, name='cinbox'),
	path('cinbox/sendmess/', views.sendmess, name="sendmess"),
	path('cinbox/fetch/', views.fetch, name="fetch"),
	path('cinbox/seen/', views.seen, name='seen'),
	path('cinbox/delete/', views.delete_mess, name='delete_mess'),
	path('createthread/', views.createthread, name='createthread'),
	path('cnotifications/', views.cnotifications, name='cnotifications'),
	path('manage_job/cjobapp/', views.jobapp, name='cjobapp'),
	path('edit_job/', views.edit_job, name='edit_job'),
	path('get_candidate', views.get_candidate, name='get_candidate'),
	path('get_cands/', views.get_cands, name='get_cands'),
	path('cand_suggest/', views.cand_suggest, name='cand_suggest'),
    path('pending_actions/', views.pending_actions, name='pending_actions'),
    path('pending_actions/cjobapp/', views.jobapp, name='cjobapp'),
	path('quiz/cjobapp/', views.jobapp, name='cjobapp'),
	path('show_tests/', views.show_tests, name='show_tests'),
	path('create_test', views.create_test, name='test'),
	path('schedule/', views.schedule, name='schedule'),
	path('test_info/', views.test_info, name='test_info'),
	path('get_results/', views.get_results, name='get_results'),
    path('schedule_interview/', views.schedule_interview, name='schedule_interview'),
    path('all_interviews/', views.all_interviews, name='all_interviews'),
    path('done/', views.done, name='done'),
    path('get_link/', views.get_link, name='get_link'),
	path('logout/', views.logout, name='clogout'),
	path('under_development/', views.under_development, name='under_development'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
