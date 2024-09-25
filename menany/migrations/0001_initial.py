# Generated by Django 5.0.6 on 2024-09-21 20:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_number', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(default='buses/default_bus.png', upload_to='buses/')),
                ('description', models.TextField(blank=True, default='No description available', null=True)),
                ('seats', models.PositiveIntegerField(default=50)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('destination', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_count', models.IntegerField()),
                ('name', models.CharField(default='Guest', max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('booking_date', models.DateField()),
                ('seats_reserved', models.IntegerField()),
                ('distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menany.bus')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menany.route')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(max_length=100)),
                ('is_paid', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menany.booking')),
            ],
        ),
        migrations.AddField(
            model_name='bus',
            name='routes',
            field=models.ManyToManyField(to='menany.route'),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('available_seats', models.PositiveIntegerField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menany.route')),
            ],
        ),
    ]
