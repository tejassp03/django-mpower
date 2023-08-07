from . import views
from django.urls import path, include 
from django.conf.urls.static import static
from django.conf import settings

app_name = 'main'

urlpatterns = [
	path('', views.index, name ='index'),
	path('blog/', views.blog, name ='blog'),
	path('user_login/', views.user_login, name ='user_login'),
	path('admin_login/', views.admin_login, name ='admin_login'),
	path('register/', views.register, name ='register'),
	path('admin_register/', views.admin_register, name ='admin_register'),
    path('subscribe/', views.subscribe, name='subscribe'),
	path('jobs/', views.findjobs, name ='jobs'),
	path('companies/', views.companies, name ='companies'),
	path('candidates/', views.candidates, name ='candidates'),
	path('postjob/', views.postjob, name ='postjob'),
    path('get_job/', views.get_job, name='get_job'),
    path('give_feedback/<int:pk>/', views.give_feedback, name='give_feedback'),
    path('give_feed/<int:pk>/', views.give_feed, name='give_feed'),
	path('profile_completion/<int:pk>/', views.profile_completion, name="profilecompletion"),
	path('emp_completion/<int:pk>/', views.emp_completion, name="emp_completion"),
	path('admin_completion/<int:pk>/', views.admin_completion, name="admin_completion"),
	path('admin_completion/<int:pk>/get_otp/', views.get_otp, name='get_otp'),
	path('admin_completion/<int:pk>/post_otp/', views.verify_otp, name='verify_otp'),
	path('profile_completion/<int:pk>/get_otp/', views.get_otp, name='get_otp'),
	path('profile_completion/<int:pk>/post_otp/', views.verify_otp, name='verify_otp'),
	path('emp_completion/<int:pk>/get_otp/', views.get_otp, name='eget_otp'),
	path('emp_completion/<int:pk>/post_otp/', views.verify_otp, name='everify_otp'),
	path('singlejob/<int:pk2>/', views.singlejob, name='singlejob'),
    path('singlecompany/<int:pk2>/', views.singlecompany, name='singlecompany'),
    path('mpoweradmin/<int:pk>/', include('mpoweradmin.urls', namespace = 'mpoweradmin')),
]

# if settings.DEBUG:
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)