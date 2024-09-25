from django.contrib import admin
from .models import Route, Bus, Booking, Payment, Schedule

class RouteAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'distance')
    search_fields = ('source', 'destination')

class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'name', 'seats', 'price')
    search_fields = ('bus_number', 'name')
    list_filter = ('routes',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'bus', 'seat_count', 'total_price', 'booking_date', 'seats_reserved')
    search_fields = ('name', 'bus__name', 'email')
    list_filter = ('booking_date',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'is_paid', 'payment_date')
    search_fields = ('booking__name', 'method')
    list_filter = ('is_paid', 'method')

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('route', 'date', 'available_seats')
    list_filter = ('route', 'date')

# Register your models here
admin.site.register(Route, RouteAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Schedule, ScheduleAdmin)
