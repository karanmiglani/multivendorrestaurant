# Generated by Django 5.0.6 on 2024-05-30 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_1',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='address_line_2',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
