# Generated by Django 5.1.7 on 2025-03-30 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Startup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('industry_type', models.CharField(choices=[('tech', 'Technology'), ('fintech', 'Fintech'), ('healthcare', 'Healthcare'), ('education', 'Education'), ('other', 'Other')], max_length=50)),
                ('years_in_business', models.PositiveIntegerField()),
                ('company_logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('annual_revenue', models.FloatField()),
                ('profit_margin', models.FloatField()),
                ('investment_required', models.FloatField()),
                ('funding_purpose', models.TextField()),
                ('target_market', models.TextField()),
                ('growth_trend', models.CharField(choices=[('growing', 'Growing'), ('stable', 'Stable'), ('declining', 'Declining')], max_length=50)),
                ('pitch_video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('business_proposal', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('legal_documents', models.FileField(blank=True, null=True, upload_to='documents/')),
            ],
        ),
    ]
