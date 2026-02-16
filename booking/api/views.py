# booking/api/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken   # works natively now
from django.utils import timezone


from booking.models import GymUser, Profile, Booking, OTP
from .serializers import (
    GymUserSerializer, ProfileSerializer,
    BookingSerializer, OTPRequestSerializer, OTPVerifySerializer
)
import random


@api_view(['POST'])
@permission_classes([AllowAny])
def request_otp(request):
    """Request an OTP for phone number verification."""
    serializer = OTPRequestSerializer(data=request.data)
    if serializer.is_valid():
        phone = serializer.validated_data['phone']

        GymUser.objects.get_or_create(phone=phone)
        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, otp=otp_code)

        print(f"[DEV] OTP for {phone}: {otp_code}")  # remove in production

        return Response({
            'message': 'OTP sent successfully',
            'phone': phone,
            'otp': otp_code  # remove in production
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """Verify OTP and return JWT tokens."""
    serializer = OTPVerifySerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        # Works perfectly — GymUser IS the Django User now
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': GymUserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access':  str(refresh.access_token),
            }
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Return the currently authenticated user."""
    return Response(GymUserSerializer(request.user).data)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class   = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # request.user is GymUser directly — clean and simple
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class   = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        bookings = self.get_queryset().filter(
            preferred_date__gte=timezone.now().date()
        )
        return Response(self.get_serializer(bookings, many=True).data)