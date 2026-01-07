from django.contrib import admin
from .models import User, Vehicle, Ride, Booking

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'make', 'model', 'plate_number', 'seats')


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'origin', 'destination', 'departure_time', 'available_seats')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'ride', 'passenger', 'seats', 'created_at')
