from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Route(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100, blank=True, null=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 

    def __str__(self):
        return f"{self.source} to {self.destination if self.destination else 'N/A'}"



class Bus(models.Model):
    bus_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='buses/', default='buses/default_bus.png')
    description = models.TextField(blank=True, null=True, default='No description available')
    routes = models.ManyToManyField(Route)
    seats = models.PositiveIntegerField(default=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Bus {self.bus_number} - {self.name}"


from django.core.exceptions import ValidationError

class Booking(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_count = models.IntegerField()
    name = models.CharField(max_length=255, default='Guest')
    email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)  # Ensure this field exists
    booking_date = models.DateField(null=True, blank=True)
    seats_reserved = models.IntegerField()
    distance = models.DecimalField(max_digits=10, decimal_places=2) 

    def save(self, *args, **kwargs):
        if self.bus is None:
            raise ValidationError("Bus cannot be None.")
        
        if self.bus.price is None:
            raise ValidationError("Bus price is missing, cannot calculate total price.")

        # Calculate total price if not set
        if not self.total_price:
            self.total_price = Decimal(self.bus.price) * Decimal(self.seat_count)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.bus.bus_number} - Seats: {self.seat_count}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=100)  # e.g., Credit Card, PayPal
    is_paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)  # Allow null values
    
    # Optional fields for additional payment details
    cc_name = models.CharField(max_length=100, blank=True, null=True)  # For Credit Card
    mpesa_phone = models.CharField(max_length=15, blank=True, null=True)  # For Mpesa
    bank_name = models.CharField(max_length=100, blank=True, null=True)  # For Bank Transfer
    # Add other fields as necessary

    def __str__(self):
        return f"Payment of {self.amount} for {self.booking}"



class Schedule(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"Schedule for {self.route} on {self.date}"
