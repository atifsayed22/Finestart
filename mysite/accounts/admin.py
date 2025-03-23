from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Add this line
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "user_types", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)

admin.site.register(CustomUser, CustomUserAdmin)