from django.contrib import admin
from .models import Company,Investor, FundingRound, Investment

# Register your models here.
admin.site.register(Company)
admin.site.register(Investor)
admin.site.register(FundingRound)
admin.site.register(Investment)

