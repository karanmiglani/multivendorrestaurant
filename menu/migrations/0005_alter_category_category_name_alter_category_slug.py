# Generated by Django 5.0.6 on 2024-05-31 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_category_unique_vendor_category_name_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(max_length=100),
        ),
    ]
