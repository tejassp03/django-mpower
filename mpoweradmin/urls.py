from . import views
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mpoweradmin'

urlpatterns = [
	path('', views.dashboard, name='cdashboard')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
