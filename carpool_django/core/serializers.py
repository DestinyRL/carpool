from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Sum
from .models import User, Vehicle, Ride, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone')
        read_only_fields = ('id',)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone')

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', '')
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    vehicles = serializers.SerializerMethodField()
    rides_count = serializers.SerializerMethodField()
    bookings_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone', 'date_joined', 'vehicles', 'rides_count', 'bookings_count')
        read_only_fields = ('id', 'date_joined', 'rides_count', 'bookings_count')

    def get_vehicles(self, obj):
        vehicles = obj.vehicles.all()
        return VehicleSerializer(vehicles, many=True).data

    def get_rides_count(self, obj):
        return obj.rides.count()

    def get_bookings_count(self, obj):
        return obj.bookings.count()


class VehicleSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Vehicle
        fields = ('id', 'owner', 'owner_username', 'make', 'model', 'plate_number', 'seats')
        read_only_fields = ('id', 'owner')

    def validate_seats(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Seats must be between 1 and 10.")
        return value


class RideSerializer(serializers.ModelSerializer):
    driver = UserSerializer(read_only=True)
    available_slots = serializers.SerializerMethodField()
    bookings_count = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = ('id', 'driver', 'vehicle', 'origin', 'destination', 'departure_time', 'available_seats', 'price_cents', 'available_slots', 'bookings_count')
        read_only_fields = ('id', 'driver')

    def validate_departure_time(self, value):
        from django.utils import timezone
        if value <= timezone.now():
            raise serializers.ValidationError("Departure time must be in the future.")
        return value

    def validate_available_seats(self, value):
        if value < 1:
            raise serializers.ValidationError("Available seats must be at least 1.")
        return value

    def validate_price_cents(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def get_available_slots(self, obj):
        booked = obj.bookings.aggregate(total=Sum('seats'))['total'] or 0
        return max(0, obj.available_seats - booked)

    def get_bookings_count(self, obj):
        return obj.bookings.count()


class BookingSerializer(serializers.ModelSerializer):
    passenger = UserSerializer(read_only=True)
    ride_details = RideSerializer(source='ride', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ('id', 'ride', 'ride_details', 'passenger', 'seats', 'total_price', 'created_at')
        read_only_fields = ('id', 'passenger', 'created_at', 'ride_details')

    def validate_seats(self, value):
        if value < 1:
            raise serializers.ValidationError("Must book at least 1 seat.")
        return value

    def validate(self, data):
        ride = data.get('ride')
        seats = data.get('seats')
        
        if ride:
            booked = ride.bookings.aggregate(total=Sum('seats'))['total'] or 0
            available = ride.available_seats - booked
            if seats > available:
                raise serializers.ValidationError(f"Only {available} seats available for this ride.")
        
        return data

    def get_total_price(self, obj):
        return obj.seats * obj.ride.price_cents
