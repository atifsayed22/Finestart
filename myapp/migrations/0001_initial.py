# Generated by Django 5.1.7 on 2025-03-22 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('industry', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('investor_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FundingRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_type', models.CharField(max_length=100)),
                ('round_date', models.DateField()),
                ('amount_raised', models.DecimalField(decimal_places=2, max_digits=15)),
                ('valuation', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funding_rounds', to='myapp.company')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_date', models.DateField()),
                ('amount_invested', models.DecimalField(decimal_places=2, max_digits=15)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='myapp.company')),
                ('funding_round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='myapp.fundinground')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='myapp.investor')),
            ],
        ),
    ]
