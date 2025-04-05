from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StartupProfile, InvestorProfile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "user_type", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("username",)
    fieldsets = UserAdmin.fieldsets + (
        ('User Type', {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Type', {'fields': ('user_type',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StartupProfile)
admin.site.register(InvestorProfile)