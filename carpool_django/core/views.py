from rest_framework import viewsets, permissions, status, filters, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Sum
from .models import User, Vehicle, Ride, Booking
from .serializers import (
    VehicleSerializer, RideSerializer, BookingSerializer,
    UserSerializer, UserRegistrationSerializer, UserProfileSerializer
)


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully", "user": UserSerializer(user).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['make', 'model', 'plate_number']
    ordering_fields = ['id', 'seats']
    ordering = ['-id']

    def get_queryset(self):
        return Vehicle.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            return Response(
                {"error": "You can only update your own vehicles"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            return Response(
                {"error": "You can only delete your own vehicles"},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_vehicles(self, request):
        vehicles = Vehicle.objects.filter(owner=request.user)
        serializer = self.get_serializer(vehicles, many=True)
        return Response(serializer.data)


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['origin', 'destination']
    ordering_fields = ['departure_time', 'price_cents']
    ordering = ['departure_time']

    def get_queryset(self):
        queryset = Ride.objects.all()
        origin = self.request.query_params.get('origin')
        destination = self.request.query_params.get('destination')
        available_only = self.request.query_params.get('available_only', 'false').lower() == 'true'

        if origin:
            queryset = queryset.filter(origin__icontains=origin)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        if available_only:
            queryset = queryset.filter(available_seats__gt=0)

        return queryset

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.driver != self.request.user:
            return Response(
                {"error": "You can only update your own rides"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.driver != self.request.user:
            return Response(
                {"error": "You can only delete your own rides"},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_rides(self, request):
        rides = Ride.objects.filter(driver=request.user)
        serializer = self.get_serializer(rides, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        ride = self.get_object()
        booked = ride.bookings.aggregate(total=Sum('seats'))['total'] or 0
        available = max(0, ride.available_seats - booked)
        return Response({
            "ride_id": ride.id,
            "total_seats": ride.available_seats,
            "booked_seats": booked,
            "available_seats": available
        })


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Booking.objects.filter(passenger=self.request.user)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)

    def perform_destroy(self, instance):
        if instance.passenger != self.request.user:
            return Response(
                {"error": "You can only cancel your own bookings"},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        bookings = Booking.objects.filter(passenger=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.passenger != request.user:
            return Response(
                {"error": "You can only cancel your own bookings"},
                status=status.HTTP_403_FORBIDDEN
            )
        booking.delete()
        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_204_NO_CONTENT)
