# Generated by Django 5.0.6 on 2024-09-23 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menany', '0003_route_distance'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='bank_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='cc_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='mpesa_phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
