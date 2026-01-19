from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VehicleViewSet, RideViewSet, BookingViewSet,
    UserRegistrationView, UserProfileView
)

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegistrationView.as_view(), name='user_register'),
    path('users/me/', UserProfileView.as_view(), name='user_profile'),
]
