import pytest
from django.urls import reverse
from booking.models import GymUser, OTP, Profile, Booking
from booking.tests.factories import (
    GymUserFactory, TrainerFactory, ProgramFactory, ProfileFactory
)


@pytest.mark.django_db
class TestSendOTPView:
    def test_get_send_otp_page(self, client):
        """Test GET request to send OTP page"""
        url = reverse('Booking:send_otp')
        response = client.get(url)
        assert response.status_code == 200
        assert b'Login with Mobile' in response.content or b'mobile' in response.content.lower()

    def test_post_send_otp_creates_user_and_otp(self, client):
        """Test POST request creates user and OTP"""
        url = reverse('Booking:send_otp')
        phone = "1234567890"
        response = client.post(url, {'phone': phone})
        
        # Check user created
        assert GymUser.objects.filter(phone=phone).exists()
        
        # Check OTP created
        assert OTP.objects.filter(phone=phone).exists()
        
        # Check session set
        assert client.session.get('otp_phone') == phone
        
        # Check redirect
        assert response.status_code == 302
        assert response.url == reverse('Booking:verify_otp')

    def test_post_send_otp_existing_user(self, client, gym_user):
        """Test POST with existing user"""
        url = reverse('Booking:send_otp')
        initial_count = GymUser.objects.count()
        
        response = client.post(url, {'phone': gym_user.phone})
        
        # Should not create new user
        assert GymUser.objects.count() == initial_count
        
        # Should create OTP
        assert OTP.objects.filter(phone=gym_user.phone).exists()


@pytest.mark.django_db
class TestVerifyOTPView:
    def test_get_verify_otp_page(self, client):
        """Test GET request to verify OTP page"""
        url = reverse('Booking:verify_otp')
        response = client.get(url)
        assert response.status_code == 200
        assert b'Verify OTP' in response.content or b'otp' in response.content.lower()

    def test_post_verify_otp_success(self, client, unverified_user):
        """Test successful OTP verification"""
        # Create OTP
        otp = OTP.objects.create(phone=unverified_user.phone, otp="123456")
        
        # Set session
        session = client.session
        session['otp_phone'] = unverified_user.phone
        session.save()
        
        url = reverse('Booking:verify_otp')
        response = client.post(url, {'otp': '123456'})
        
        # Check user is verified
        unverified_user.refresh_from_db()
        assert unverified_user.is_verified is True
        
        # Check session
        assert client.session.get('user_id') == unverified_user.id
        assert 'otp_phone' not in client.session
        
        # Check redirect
        assert response.status_code == 302
        assert response.url == reverse('Booking:booking')

    def test_post_verify_otp_invalid(self, client, unverified_user):
        """Test invalid OTP"""
        otp = OTP.objects.create(phone=unverified_user.phone, otp="123456")
        
        session = client.session
        session['otp_phone'] = unverified_user.phone
        session.save()
        
        url = reverse('Booking:verify_otp')
        response = client.post(url, {'otp': '999999'})
        
        # Should redirect back to verify
        assert response.status_code == 302
        assert response.url == reverse('Booking:verify_otp')
        
        # User should not be verified
        unverified_user.refresh_from_db()
        assert unverified_user.is_verified is False

    def test_post_verify_otp_expired(self, client, unverified_user):
        """Test expired OTP"""
        from django.utils import timezone
        from datetime import timedelta
        
        otp = OTP.objects.create(phone=unverified_user.phone, otp="123456")
        otp.created_at = timezone.now() - timedelta(minutes=6)
        otp.save()
        
        session = client.session
        session['otp_phone'] = unverified_user.phone
        session.save()
        
        url = reverse('Booking:verify_otp')
        response = client.post(url, {'otp': '123456'})
        
        # Should redirect to send OTP
        assert response.status_code == 302
        assert response.url == reverse('Booking:send_otp')


@pytest.mark.django_db
class TestBookingView:
    def test_get_booking_page_unauthenticated(self, client):
        """Test GET without authentication redirects to login"""
        url = reverse('Booking:booking')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('Booking:send_otp')

    def test_get_booking_page_authenticated(self, authenticated_session, trainer, program):
        """Test GET with authentication"""
        url = reverse('Booking:booking')
        response = authenticated_session.get(url)
        assert response.status_code == 200
        assert b'booking' in response.content.lower() or b'book' in response.content.lower()

    def test_post_create_booking(self, authenticated_session, gym_user, trainer, program):
        """Test creating a booking"""
        url = reverse('Booking:booking')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'program': program.id,
            'trainer': trainer.id,
            'date': '2026-02-15',
            'time': 'morning',
            'message': 'Looking forward!'
        }
        response = authenticated_session.post(url, data)
        
        # Check booking created
        assert Booking.objects.filter(user=gym_user).exists()
        booking = Booking.objects.get(user=gym_user)
        assert booking.user_name == 'Test User'
        assert booking.program == program
        assert booking.trainer == trainer
        
        # Check profile created/updated
        assert Profile.objects.filter(user=gym_user).exists()
        
        # Check redirect
        assert response.status_code == 302

    def test_post_booking_missing_fields(self, authenticated_session, program):
        """Test booking with missing required fields"""
        url = reverse('Booking:booking')
        data = {
            'name': 'Test User',
            # Missing email, program, date, time
        }
        response = authenticated_session.post(url, data)
        
        # Should redirect back
        assert response.status_code == 302
        assert response.url == reverse('Booking:booking')
        
        # No booking should be created
        assert Booking.objects.count() == 0


@pytest.mark.django_db
class TestProfileView:
    def test_get_profile_unauthenticated(self, client):
        """Test GET profile without authentication"""
        url = reverse('Booking:profile')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == reverse('Booking:send_otp')

    def test_get_profile_authenticated(self, authenticated_session, profile):
        """Test GET profile with authentication"""
        url = reverse('Booking:profile')
        response = authenticated_session.get(url)
        assert response.status_code == 200
        assert b'Profile' in response.content or b'profile' in response.content.lower()

    def test_post_update_profile(self, authenticated_session, gym_user):
        """Test updating profile"""
        # Create initial profile
        profile = ProfileFactory(user=gym_user)
        
        url = reverse('Booking:profile')
        data = {
            'name': 'Updated Name',
            'email': 'updated@example.com',
            'height': '180.5',
            'weight': '75.0',
            'emergency_contact': '9999999999',
            'medical_notes': 'Updated notes'
        }
        response = authenticated_session.post(url, data)
        
        # Check profile updated
        profile.refresh_from_db()
        assert profile.name == 'Updated Name'
        assert profile.email == 'updated@example.com'
        assert float(profile.height) == 180.5
        assert float(profile.weight) == 75.0
        
        # Check redirect
        assert response.status_code == 302
        assert response.url == reverse('Booking:profile')

    def test_profile_displays_bookings(self, authenticated_session, booking):
        """Test profile displays user bookings"""
        url = reverse('Booking:profile')
        response = authenticated_session.get(url)
        assert response.status_code == 200
        # Check booking info in response
        assert booking.program.title.encode() in response.content


@pytest.mark.django_db
class TestLogoutView:
    def test_logout(self, authenticated_session):
        """Test logout functionality"""
        # Verify user is logged in
        assert 'user_id' in authenticated_session.session
        
        url = reverse('Booking:logout')
        response = authenticated_session.get(url)
        
        # Check session cleared
        assert 'user_id' not in authenticated_session.session
        
        # Check redirect
        assert response.status_code == 302
        assert response.url == reverse('Booking:send_otp')
        
# booking/tests/test_views.py — ADD these new classes

@pytest.mark.django_db
class TestJWTAuthentication:
    """Tests specific to JWT auth flow"""

    def test_verify_otp_returns_jwt_tokens(self, api_client):
        """OTP verification returns both access and refresh tokens"""
        phone = "5551234567"
        GymUser.objects.create_user(phone=phone)
        OTP.objects.create(phone=phone, otp="123456")

        url = reverse('verify-otp')
        response = api_client.post(url, {
            "phone": phone, "otp": "123456"
        }, format='json')

        assert response.status_code == 200
        assert 'tokens' in response.data
        assert 'access' in response.data['tokens']
        assert 'refresh' in response.data['tokens']

    def test_protected_endpoint_with_valid_token(
        self, authenticated_api_client
    ):
        """Valid JWT allows access to protected endpoint"""
        url = reverse('current-user')
        response = authenticated_api_client.get(url)
        assert response.status_code == 200

    def test_protected_endpoint_without_token(self, api_client):
        """No token returns 401"""
        url = reverse('current-user')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_protected_endpoint_with_fake_token(self, api_client):
        """Fake token returns 401"""
        api_client.credentials(
            HTTP_AUTHORIZATION='Bearer thisisafaketoken'
        )
        url = reverse('current-user')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_refresh_token_returns_new_access(self, api_client):
        """Refresh endpoint issues new access token"""
        phone = "5559876543"
        GymUser.objects.create_user(phone=phone)
        OTP.objects.create(phone=phone, otp="654321")

        # Get initial tokens
        token_response = api_client.post(
            reverse('verify-otp'),
            {"phone": phone, "otp": "654321"},
            format='json'
        )
        refresh_token = token_response.data['tokens']['refresh']

        # Refresh
        response = api_client.post(
            reverse('token-refresh'),
            {"refresh": refresh_token},
            format='json'
        )
        assert response.status_code == 200
        assert 'access' in response.data


@pytest.mark.django_db
class TestAdminUserBehavior:
    """Tests specific to superuser/admin behavior"""

    def test_superuser_has_usable_password(self, admin_user):
        """Admin can authenticate with password"""
        assert admin_user.has_usable_password()
        assert admin_user.check_password("admin123")

    def test_member_has_unusable_password(self, gym_user):
        """Member cannot authenticate with password"""
        assert not gym_user.has_usable_password()

    def test_admin_is_staff(self, admin_user):
        assert admin_user.is_staff is True

    def test_member_is_not_staff(self, gym_user):
        assert gym_user.is_staff is False