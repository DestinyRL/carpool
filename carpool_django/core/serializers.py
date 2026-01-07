from rest_framework import serializers
from .models import User, Vehicle, Ride, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone')


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class RideSerializer(serializers.ModelSerializer):
    driver = UserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    passenger = UserSerializer(read_only=True)
    ride = RideSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
