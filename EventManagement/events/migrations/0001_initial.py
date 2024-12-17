# Generated by Django 3.1.12 on 2024-12-01 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='event_images/')),
                ('planning_image', models.ImageField(blank=True, null=True, upload_to='event_images/')),
                ('planning_description', models.TextField(blank=True, null=True)),
                ('management_image', models.ImageField(blank=True, null=True, upload_to='event_images/')),
                ('management_description', models.TextField(blank=True, null=True)),
                ('technologies_image', models.ImageField(blank=True, null=True, upload_to='event_images/')),
                ('technologies_description', models.TextField(blank=True, null=True)),
                ('pricing', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_section', models.CharField(default='General Admission', max_length=200)),
                ('num_tickets', models.PositiveIntegerField(default=1)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('ticket_number', models.CharField(max_length=50, unique=True)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]