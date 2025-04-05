from django.db import models

# Create your models here.
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Investor(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    investor_type = models.CharField(max_length=100)  # e.g., Angel, VC, Corporate

    def __str__(self):
        return self.name

class FundingRound(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="funding_rounds")
    round_type = models.CharField(max_length=100)  # e.g., Seed, Series A, Series B
    round_date = models.DateField()
    amount_raised = models.DecimalField(max_digits=15, decimal_places=2)
    valuation = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.company.name} - {self.round_type}"

class Investment(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="investments")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="investments")
    funding_round = models.ForeignKey(FundingRound, on_delete=models.CASCADE, related_name="investments")
    investment_date = models.DateField()
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.investor.name} invested in {self.company.name}"