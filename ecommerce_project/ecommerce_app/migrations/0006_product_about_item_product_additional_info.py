# Generated by Django 5.1.2 on 2024-11-13 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0005_remove_product_about_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='about_item',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='additional_info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
