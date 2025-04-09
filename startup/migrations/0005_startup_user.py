# Generated by Django 5.1.7 on 2025-04-08 16:17

import django.db.models.deletion
import startup.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0004_alter_startup_industry_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='user',
            field=models.ForeignKey(default=startup.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, related_name='startups', to=settings.AUTH_USER_MODEL),
        ),
    ]
