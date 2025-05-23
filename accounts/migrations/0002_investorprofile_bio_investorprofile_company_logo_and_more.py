# Generated by Django 5.1.4 on 2025-04-08 20:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='investorprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='investorprofile',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='investor_logos/'),
        ),
        migrations.AddField(
            model_name='investorprofile',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='investorprofile',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='investorprofile',
            name='investment_focus',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='investorprofile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='investorprofile',
            name='portfolio_size',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='investorprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='investor_profiles/'),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='business_model',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='ceo_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='company_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='equity_structure',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='monthly_profit',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='startup_stage',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='startupprofile',
            name='team_size',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
