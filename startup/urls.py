from django.urls import path
from . import views

app_name = 'startup'

urlpatterns = [
    path('register/', views.startup_registration, name='startup_registration'),
    path('dashboard/', views.startup_dashboard, name='startup_dashboard'),
    path('insights/', views.startup_insights, name='startup_insights'),
    path('profile/', views.startup_profile, name='startup_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('find_investors/', views.find_investors, name='find_investors'),
    path('connect_with_investor/<int:investor_id>/', views.connect_with_investor, name='connect_with_investor'),
    path('upload_pitch/', views.startup_upload_pitch, name='startup_upload_pitch'),
    path('manage_offers/', views.manage_offers, name='manage_offers'),
    path('create_offer/<int:startup_id>/', views.create_offer, name='create_offer'),
    path('respond_to_offer/<int:offer_id>/<str:response>/', views.respond_to_offer, name='respond_to_offer'),
    path('find_startups/', views.find_startups, name='find_startups'),
    path('add_profit_entry/', views.add_profit_entry, name='add_profit_entry'),
    path('delete_profit_entry/', views.delete_profit_entry, name='delete_profit_entry'),
    path('profit_data/', views.profit_data, name='profit_data'),
]
