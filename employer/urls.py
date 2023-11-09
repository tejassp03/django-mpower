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
	path('all_templates/', views.all_templates, name='all_templates'),
    path('create_temp/', views.create_temp, name='create_temp'),
    path('get_template/', views.get_template, name='get_template'),
	path('schedule_temp/', views.schedule_temp, name='schedule_temp'),
    path('edit_template/<int:pk2>/', views.edit_template, name='edit_template'),
    path('get_temp_details/', views.get_temp_details, name='get_temp_details'),
    path('get_all_steps/<int:pk2>/', views.get_all_steps, name='get_all_steps'),
    path('delastep/<int:pk2>/', views.delastep, name='delastep'),
    path('all_steps/', views.all_steps, name='all_steps'),
    path('create_step/', views.create_step, name='create_step'),
    path('get_step/', views.get_step, name='get_step'),
    path('edit_step/', views.edit_step, name='edit_step'),
    path('done/', views.done, name='done'),
    path('get_link/', views.get_link, name='get_link'),
	path('logout/', views.logout, name='clogout'),
	path('suggest/', views.suggest, name='suggest'),
	path('request_cand/', views.requestCand, name='requestCand'),
	path('interview_complete/', views.interview_complete, name='interview_complete'),
	path('panel_request/', views.panel_request, name='panel_request'),
	path('edit_test/', views.edit_test, name='edit_test'),
	path('resume_feedback/', views.resume_feedback, name='resume_feedback'),
	path('matchPerChange/', views.matchPerChange, name='matchPerChange'),
	path('under_development/', views.under_development, name='under_development'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
