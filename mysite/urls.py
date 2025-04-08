"""
URL configuration for mysite project.
"""
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('base/', views.base),
    path('demo/', views.demo),
    path('startup/', include('startup.urls', namespace='startup')),
    path('accounts/', include('accounts.urls')),
    path('investor/', include('investor.urls')),
]
