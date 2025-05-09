# Generated by Django 5.1.4 on 2025-04-08 21:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_investorprofile_bio_investorprofile_company_logo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyProfit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.FloatField(default=0)),
                ('startup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profit_records', to='accounts.startupprofile')),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('startup', 'date')},
            },
        ),
    ]
