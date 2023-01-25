from . import views
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'candidate'

urlpatterns = [
	path('', views.dashboard, name ='dashboard'),
	path('jobapp/', views.jobapp, name='jobapp'),
	path('count_inbox/', views.count_inbox, name='count_inbox'),
	path('edit_profile/', views.edit_profile, name='edit'),
	path('edit_profile/add_skill/', views.add_skill, name='add_skill'),
	path('edit_profile/add_exp/', views.add_exp, name='add_exp'),
	path('edit_profile/add_edu/', views.add_edu, name='add_edu'),
	path('edit_profile/delete_exp/', views.delete_exp, name='delete_exp'),
	path('edit_profile/delete_skill/', views.delete_skill, name='delete_skill'),
	path('edit_profile/delete_edu/', views.delete_edu, name='delete_edu'),
	path('under_development/', views.under_development, name='under_development'),
	path('inbox/', views.inbox, name='inbox'),
	path('<int:pk2>/', views.employer, name='employer'),
	path('<int:pk2>/startconver/<pk3>/', views.startconver, name='startconver'),
	path('<int:pk2>/startconver/<pk3>/send', views.send, name='send'),
	path('inbox/sendfrom/', views.sendfromcand, name="sendfrom"),
	path('inbox/fetchmess/', views.fetchmess, name="fetchmess"),
	path('inbox/seenmes/', views.seenmes, name='seenmes'),
	path('resume/', views.resume, name='resume'),
	path('logout/', views.logout, name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)