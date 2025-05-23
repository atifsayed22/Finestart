from django.urls import path
from . import views

app_name = 'investor'

urlpatterns = [
    path('dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('discover/', views.startup_discovery, name='startup_discovery'),
    path('portfolio/', views.portfolio_tracker, name='portfolio_tracker'),
    path('profile/', views.investor_profile, name='investor_profile'),
    path('find_startups/', views.find_startups, name='find_startups'),
    path('offer/<int:offer_id>/', views.view_offer, name='view_offer'),
    path('offer/<int:offer_id>/edit/', views.edit_offer, name='edit_offer'),
    path('create_offer/', views.create_offer, name='create_offer'),
] 