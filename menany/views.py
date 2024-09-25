from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Bus 
from datetime import date
from django.urls import reverse
from .models import Booking, Payment, Schedule, Route
from django.core.exceptions import ValidationError


# Home view
def home(request):
    return render(request, 'home.html')

# Services view
def services(request):
    return render(request, 'services.html')

# About view
def about(request):
    return render(request, 'about.html')

# Buses view
def buses(request):
    return render(request, 'buses.html')

# Blog view
def blog(request):
    return render(request, 'blog.html')

# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        messages.success(request, "Signup successful! Please login.")
        return redirect('login')
    return render(request, 'signup.html')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('buses')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
    return render(request, 'login.html')




def buses(request):
    buses = Bus.objects.all()  # Fetch all Bus objects
    return render(request, 'buses.html', {'buses': buses})

def booking(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    routes = Route.objects.all()  # Fetch available routes
    
    if request.method == 'POST':
        seat_count = int(request.POST.get('seat_count'))
        route_id = request.POST.get('route')
        route = get_object_or_404(Route, id=route_id)
        name = request.POST.get('name', 'Guest')
        email = request.POST.get('email')

        # Calculate the total price (bus price * seat_count)
        total_price = Decimal(bus.price) * Decimal(seat_count)

        # Save the booking
        booking = Booking(
            bus=bus,
            seat_count=seat_count,
            name=name,
            email=email,
            total_price=total_price,
            route=route,
            booking_date=timezone.now(),  # Use the current date as the booking date
            seats_reserved=seat_count,
            distance=route.distance
        )
        try:
            booking.save()
            return redirect('confirmation', booking_id=booking.id)  # Redirect to confirmation page
        except ValidationError as e:
            return render(request, 'booking.html', {
                'bus': bus,
                'routes': routes,
                'error': str(e),
            })

    return render(request, 'booking.html', {'bus': bus, 'routes': routes})

def confirmation(request, booking_id):
    # Debugging output to check the requested booking ID
    print("Requested booking ID:", booking_id)
    
    # Fetch existing booking IDs for debugging
    existing_bookings = Booking.objects.values_list('id', flat=True)
    print("Existing booking IDs:", list(existing_bookings))
    
    # Try to get the specific booking based on the booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Retrieve related bus information
    bus = get_object_or_404(Bus, id=booking.bus.id)  # Assuming bus_id is accessible via bus relationship

    # Get user details
    user_name = request.user.username  # Get the user's name
    user_email = request.user.email  # Get the user's email

    # Prepare context for rendering
    context = {
        'bus': bus,
        'user_name': user_name,
        'seat_count': booking.seat_count,
        'total_price': booking.total_price,
        'booking_date': booking.booking_date,
        'user_email': user_email,
        'booking_id': booking.id,  # Pass the booking ID for payment URL
    }
    
    return render(request, 'confirmation.html', context)


def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        method = request.POST.get('method')
        amount = request.POST.get('amount')

        if not amount:
            messages.error(request, 'Amount is required.')
            return redirect('payment', booking_id=booking_id)

        # Here you should handle each payment method accordingly
        if method == "Credit Card":
            # Handle credit card processing
            cc_name = request.POST.get('cc-name')
            cc_number = request.POST.get('cc-number')
            cc_expiry = request.POST.get('cc-expiry')
            cc_cvv = request.POST.get('cc-cvv')
            # Validate and process the payment
        elif method == "Mpesa":
            # Handle M-Pesa processing
            mpesa_phone = request.POST.get('mpesa-phone')
            # Validate and process the payment
        elif method == "Bank Transfer":
            # Handle bank transfer processing
            bank_name = request.POST.get('bank-name')
            account_number = request.POST.get('account-number')
            routing_number = request.POST.get('routing-number')
            # Validate and process the payment

        # After processing payment
        payment_instance = Payment(booking=booking, amount=amount, method=method)
        payment_instance.is_paid = True  # Simulate successful payment
        payment_instance.save()
        
        messages.success(request, 'Payment confirmed! Redirecting to your bookings.')
        return redirect('success', booking_id=booking.id)

    return render(request, 'payment.html', {'booking': booking})



def schedule(request, bus_id):
    # Ensure the bus exists using get_object_or_404
    bus = get_object_or_404(Bus, id=bus_id)
    
    # Handle POST request for creating a new schedule
    if request.method == 'POST':
        # Fetch form data from POST request
        route_id = request.POST.get('route_id')
        booking_date = request.POST.get('date')  # Use the correct field name from your model
        seats_reserved = request.POST.get('available_seats')

        # Ensure the route exists using get_object_or_404
        bus = get_object_or_404(Bus, id=bus_id)
        route = get_object_or_404(Route, id=route_id)

        # Create a new schedule entry
        booking = Booking.objects.create(
            bus=bus,
            route=route,
            booking_date=booking_date,  # Use 'booking_date' instead of 'date'
            seats_reserved=seats_reserved  # Use 'seats_reserved' instead of 'available_seats'
        )

        # Redirect to home or a success page after creation
        return redirect('payment', booking_id=booking.id)

    # For GET request, display schedules related to the bus
    schedules = Schedule.objects.filter(route__bus=bus)  # Proper ForeignKey lookup
    routes = Route.objects.filter(bus=bus)

    # Render the schedule template, passing the filtered schedules and routes
    return render(request, 'schedule.html', {
        'schedules': schedules,
        'routes': routes,
        'bus': bus
    })


def success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'success.html', {'booking': booking})
