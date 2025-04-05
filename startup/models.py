from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="companies")

    def __str__(self):
        return self.name
    
class Investor(models.Model):
    
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    investor_type = models.CharField(max_length=100)  # e.g., Angel, VC, Corporate
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="investors")

    def __str__(self):
        return self.name
    

class Startup(models.Model):
    INDUSTRY_CHOICES = [
        ('tech', 'Technology'),
        ('fintech', 'Fintech'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('other', 'Other'),
        
    ]

    GROWTH_TREND_CHOICES = [
        ('growing', 'Growing'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
    ]

    name = models.CharField(max_length=255)
    industry_type = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    years_in_business = models.PositiveIntegerField()
    company_logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    annual_revenue = models.FloatField()
    profit_margin = models.FloatField()
    investment_required = models.FloatField()
    funding_purpose = models.TextField()

    target_market = models.TextField()
    growth_trend = models.CharField(max_length=50, choices=GROWTH_TREND_CHOICES)
    pitch_video = models.FileField(upload_to='videos/', blank=True, null=True)

    business_proposal = models.FileField(upload_to='documents/', blank=True, null=True)
    legal_documents = models.FileField(upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return self.name
