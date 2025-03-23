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