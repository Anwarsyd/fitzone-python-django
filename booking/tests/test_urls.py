import pytest
from django.urls import reverse, resolve
from booking import views


class TestBookingURLs:
    """Test URL patterns for booking app"""

    def test_booking_url(self):
        """Test booking URL resolves correctly"""
        url = reverse('Booking:booking')
        assert url == '/booking/'
        assert resolve(url).func.view_class == views.BookingView

    def test_send_otp_url(self):
        """Test send OTP URL resolves correctly"""
        url = reverse('Booking:send_otp')
        assert url == '/booking/login/'
        assert resolve(url).func.view_class == views.SendOTPView

    def test_verify_otp_url(self):
        """Test verify OTP URL resolves correctly"""
        url = reverse('Booking:verify_otp')
        assert url == '/booking/verify-otp/'
        assert resolve(url).func.view_class == views.VerifyOTPView

    def test_profile_url(self):
        """Test profile URL resolves correctly"""
        url = reverse('Booking:profile')
        assert url == '/booking/profile/'
        assert resolve(url).func.view_class == views.ProfileView

    def test_logout_url(self):
        """Test logout URL resolves correctly"""
        url = reverse('Booking:logout')
        assert url == '/booking/logout/'
        assert resolve(url).func == views.logout_view