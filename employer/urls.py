from . import views
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'employer'

urlpatterns = [
	path('', views.dashboard, name='cdashboard'),
	path('newjob/', views.newjob, name='newjob'),
	path('under_development/', views.under_development, name='under_development'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
