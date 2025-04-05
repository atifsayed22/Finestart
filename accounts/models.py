from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('startup', 'Startup'),
        ('investor', 'Investor'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='startup') 
    is_verified = models.BooleanField(default=False) 

    # Fixing conflicts by adding related_name
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",
        blank=True,
    )

    def __str__(self):
        return self.username

class StartupProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    startup_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)  # Add this field

class InvestorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    investor_type = models.CharField(max_length=100)  # Add this field
    investment_range = models.CharField(max_length=100)  # Add this field
