from django.contrib import admin
from .models import Company, Investor

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'website', 'owner']
    search_fields = ['name', 'industry']
    list_filter = ['industry']

@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'investor_type', 'owner']
    search_fields = ['name', 'email']
    list_filter = ['investor_type']
