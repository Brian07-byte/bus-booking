# Generated by Django 5.0.6 on 2024-09-21 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menany', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]