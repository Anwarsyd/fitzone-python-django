from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProfileViewSet, BookingViewSet,
    request_otp, verify_otp, current_user
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/request-otp/', request_otp, name='request-otp'),
    path('auth/verify-otp/', verify_otp, name='verify-otp'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/me/', current_user, name='current-user'),
]