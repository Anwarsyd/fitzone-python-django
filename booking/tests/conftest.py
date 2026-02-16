# booking/tests/conftest.py

import pytest
from django.test import Client
from rest_framework.test import APIClient
from booking.models import GymUser, OTP, Profile, Booking
from gym.models import Trainer, Program


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_client():
    """Unauthenticated API client"""
    return APIClient()


# ─────────────────────────────────────────
# CHANGED: use GymUser.objects.create_user()
# instead of GymUser.objects.create()
# ─────────────────────────────────────────
@pytest.fixture
def gym_user(db):
    """Verified gym member — OTP-based, no usable password"""
    return GymUser.objects.create_user(
        phone="1234567890",
        email="test@example.com",
    )


@pytest.fixture
def verified_user(db):
    """Explicitly verified user"""
    user = GymUser.objects.create_user(phone="1111111111")
    user.is_verified = True
    user.save()
    return user


@pytest.fixture
def unverified_user(db):
    """User who hasn't verified OTP yet"""
    return GymUser.objects.create_user(phone="9876543210")


# ─────────────────────────────────────────
# NEW: superuser fixture
# ─────────────────────────────────────────
@pytest.fixture
def admin_user(db):
    """Admin user with real password for admin panel"""
    return GymUser.objects.create_superuser(
        phone="0000000000",
        email="admin@fitzone.com",
        password="admin123"
    )


@pytest.fixture
def otp_instance(db, unverified_user):
    return OTP.objects.create(
        phone=unverified_user.phone,
        otp="123456"
    )


@pytest.fixture
def profile(db, gym_user):
    return Profile.objects.create(
        user=gym_user,
        name="Test User",
        email="test@example.com",
        height=175.5,
        weight=70.5,
        emergency_contact="9999999999",
        medical_notes="No allergies"
    )


@pytest.fixture
def trainer(db):
    return Trainer.objects.create(
        name="John Trainer",
        specialization="Strength Training",
        experience=5
    )


@pytest.fixture
def program(db):
    return Program.objects.create(
        title="Cardio Blast",
        description="High intensity cardio workout",
        duration="3 months",
    )


@pytest.fixture
def booking(db, gym_user, trainer, program):
    return Booking.objects.create(
        user=gym_user,
        user_name="Test User",
        user_phone=gym_user.phone,
        trainer=trainer,
        program=program,
        preferred_date="2026-06-01",
        preferred_time="morning",
        message="Looking forward to it!"
    )


# ─────────────────────────────────────────
# CHANGED: session still works the same way
# but now gym_user is a proper AbstractBaseUser
# ─────────────────────────────────────────
@pytest.fixture
def authenticated_session(client, gym_user):
    """Web session authentication"""
    session = client.session
    session['user_id'] = gym_user.id
    session.save()
    return client


# ─────────────────────────────────────────
# NEW: JWT-based API authentication
# ─────────────────────────────────────────
@pytest.fixture
def authenticated_api_client(gym_user):
    """API client with valid JWT token"""
    from rest_framework_simplejwt.tokens import RefreshToken

    # Works because GymUser extends AbstractBaseUser
    refresh = RefreshToken.for_user(gym_user)

    api = APIClient()
    api.credentials(
        HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
    )
    return api


@pytest.fixture
def admin_api_client(admin_user):
    """API client authenticated as admin"""
    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(admin_user)
    api = APIClient()
    api.credentials(
        HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
    )
    return api