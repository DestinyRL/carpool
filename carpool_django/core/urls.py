from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, RideViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'rides', RideViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
