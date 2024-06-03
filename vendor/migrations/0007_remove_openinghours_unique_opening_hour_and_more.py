# Generated by Django 5.0.6 on 2024-06-02 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_alter_openinghours_day'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='openinghours',
            name='unique_opening_hour',
        ),
        migrations.AddConstraint(
            model_name='openinghours',
            constraint=models.UniqueConstraint(fields=('vendor', 'day'), name='unique_opening_hour'),
        ),
    ]