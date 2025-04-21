from django.db import models
from accounts.models import CustomUser, InvestorProfile
from django.conf import settings

# Create your models here.
def get_default_user():
    # Return the first user as the default, or None if no users exist
    try:
        return CustomUser.objects.first().id if CustomUser.objects.exists() else None
    except Exception as e:
        print(f"Error getting default user: {e}")
        return None

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

    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='startups',
        null=True,
        blank=True
    )

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

    def get_logo_url(self):
        """Return the URL of the company logo, if it exists."""
        if self.company_logo and hasattr(self.company_logo, 'url'):
            return self.company_logo.url
        return ""
        
    def get_pitch_video_url(self):
        """Return the URL of the pitch video, if it exists."""
        if self.pitch_video and hasattr(self.pitch_video, 'url'):
            return self.pitch_video.url
        return ""
        
    def get_business_proposal_url(self):
        """Return the URL of the business proposal, if it exists."""
        if self.business_proposal and hasattr(self.business_proposal, 'url'):
            return self.business_proposal.url
        return ""
        
    def get_legal_documents_url(self):
        """Return the URL of the legal documents, if it exists."""
        if self.legal_documents and hasattr(self.legal_documents, 'url'):
            return self.legal_documents.url
        return ""

class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    investor = models.ForeignKey(InvestorProfile, on_delete=models.CASCADE, related_name='offers')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='offers')
    equity_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage of equity offered")
    investment_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount of investment offered", default=0)
    details = models.TextField(blank=True, null=True, help_text="Additional details of the offer")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewed_by_startup = models.BooleanField(default=False, help_text="Whether the startup has viewed this offer since the last update")
    response_date = models.DateTimeField(null=True, blank=True, help_text="When the startup responded to the offer")

    def __str__(self):
        return f"Offer from {self.investor.user.get_full_name()} to {self.startup.name}"
