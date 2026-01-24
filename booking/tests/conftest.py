import pytest
from django.test import Client
from booking.models import GymUser, OTP, Profile, Booking
from gym.models import Trainer, Program


@pytest.fixture
def client():
    """Django test client"""
    return Client()


@pytest.fixture
def gym_user(db):
    """Create a verified gym user"""
    user = GymUser.objects.create(
        phone="1234567890",
        email="test@example.com",
        is_verified=True
    )
    return user


@pytest.fixture
def unverified_user(db):
    """Create an unverified gym user"""
    user = GymUser.objects.create(
        phone="9876543210",
        email="unverified@example.com",
        is_verified=False
    )
    return user


@pytest.fixture
def otp_instance(db, unverified_user):
    """Create an OTP for testing"""
    otp = OTP.objects.create(
        phone=unverified_user.phone,
        otp="123456"
    )
    return otp


@pytest.fixture
def profile(db, gym_user):
    """Create a user profile"""
    profile = Profile.objects.create(
        user=gym_user,
        name="Test User",
        email="test@example.com",
        height=175.5,
        weight=70.5,
        emergency_contact="9999999999",
        medical_notes="No allergies"
    )
    return profile


@pytest.fixture
def trainer(db):
    """Create a trainer instance"""
    trainer = Trainer.objects.create(
        name="John Trainer",
        specialization="Strength Training",
        experience=5
    )
    return trainer


@pytest.fixture
def program(db):
    """Create a program instance"""
    program = Program.objects.create(
        title="Cardio Blast",
        description="High intensity cardio workout"
    )
    return program


@pytest.fixture
def booking(db, gym_user, trainer, program):
    """Create a booking instance"""
    booking = Booking.objects.create(
        user=gym_user,
        user_name="Test User",
        user_phone=gym_user.phone,
        trainer=trainer,
        program=program,
        preferred_date="2026-02-01",
        preferred_time="morning",
        message="Looking forward to it!"
    )
    return booking


@pytest.fixture
def authenticated_session(client, gym_user):
    """Create an authenticated session"""
    session = client.session
    session['user_id'] = gym_user.id
    session.save()
    return client