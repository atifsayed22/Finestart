from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('discover/', views.startup_discovery, name='startup_discovery'),
    path('portfolio/', views.portfolio_tracker, name='portfolio_tracker'),
    path('profile/', views.investor_profile, name='investor_profile'),
] 