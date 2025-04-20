from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime


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
    industry = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    monthly_profit = models.FloatField(default=0)
    team_size = models.PositiveIntegerField(default=1)
    ceo_name = models.CharField(max_length=255, blank=True, null=True)
    startup_stage = models.CharField(max_length=100, blank=True, null=True)
    equity_structure = models.TextField(blank=True, null=True)
    business_model = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    
    # Contact information fields
    website = models.URLField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.startup_name
    
    def get_monthly_profits(self, months=6):
        """Get monthly profit data for the last X months"""
        profits = []
        labels = []
        
        try:
            # Try to get real profit records from the database
            profit_records = MonthlyProfit.objects.filter(
                startup=self
            ).order_by('-date')[:months]
            
            # If we have records, use them
            if profit_records.exists():
                for record in reversed(list(profit_records)):
                    profits.append(round(record.amount, 2))
                    labels.append(record.date.strftime('%b %Y'))
            else:
                # If no records exist, generate sample data
                self._generate_sample_profits(profits, labels, months)
        except:
            # If any error occurs (like table not existing), generate sample data
            self._generate_sample_profits(profits, labels, months)
        
        return {
            'labels': labels,
            'values': profits
        }

    def _generate_sample_profits(self, profits, labels, months):
        """Generate sample profit data for charting"""
        current_month = timezone.now()
        for i in range(months):
            month = current_month - datetime.timedelta(days=30*i)
            # Start with current month's profit and slightly vary it
            variance = 0.9 + (i * 0.05)
            # For growing trend, multiply by (1 + i*0.1)
            profit_value = self.monthly_profit * variance * (1 + i*0.05)
            profits.append(round(profit_value, 2))
            labels.append(month.strftime('%b %Y'))
        
        # Reverse to show chronological order
        profits.reverse()
        labels.reverse()

class MonthlyProfit(models.Model):
    """Model to track monthly profit for startups"""
    startup = models.ForeignKey(StartupProfile, on_delete=models.CASCADE, related_name='profit_records')
    date = models.DateField()
    amount = models.FloatField(default=0)
    
    class Meta:
        unique_together = ('startup', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.startup.startup_name} - {self.date.strftime('%b %Y')}: ${self.amount}"

class InvestorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    investor_type = models.CharField(max_length=100)
    investment_range = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='investor_profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_logo = models.ImageField(upload_to='investor_logos/', blank=True, null=True)
    investment_focus = models.TextField(blank=True, null=True)
    portfolio_size = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username}'s Investor Profile"
