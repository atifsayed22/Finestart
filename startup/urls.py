from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.startup_registration, name='startup_registration'),
    path('dashboard/', views.startup_dashboard, name='startup_dashboard'),
    path('insights/', views.startup_insights, name='startup_insights'),
    path('profile/', views.startup_profile, name='startup_profile'),
    path('find_investors/', views.find_investors, name='find_investors'),
    path('upload_pitch/', views.startup_upload_pitch, name='startup_upload_pitch'),
]
