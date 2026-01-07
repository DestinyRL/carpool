from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=30, blank=True)


class Vehicle(models.Model):
    owner = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=50)
    seats = models.PositiveIntegerField(default=4)

    def __str__(self):
        return f"{self.make} {self.model} ({self.plate_number})"


class Ride(models.Model):
    driver = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='rides')
    vehicle = models.ForeignKey('core.Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    available_seats = models.PositiveIntegerField(default=1)
    price_cents = models.IntegerField(default=0)

    def __str__(self):
        return f"Ride {self.id} from {self.origin} to {self.destination}"


class Booking(models.Model):
    ride = models.ForeignKey('core.Ride', on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey('core.User', on_delete=models.CASCADE, related_name='bookings')
    seats = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} for ride {self.ride_id} by {self.passenger.username}"
