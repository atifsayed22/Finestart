from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="login"),
    path("startup_profile/", views.startup_profile, name="startup_profile"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('admin',admin.site.urls),
]
