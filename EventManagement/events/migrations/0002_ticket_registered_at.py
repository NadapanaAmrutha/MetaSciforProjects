# Generated by Django 3.1.12 on 2024-12-01 11:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='registered_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
