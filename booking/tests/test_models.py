import pytest
from django.utils import timezone
from datetime import timedelta
from booking.models import GymUser, OTP, Profile, Booking
from booking.tests.factories import (
    GymUserFactory, OTPFactory, ProfileFactory, 
    BookingFactory, TrainerFactory, ProgramFactory
)


@pytest.mark.django_db
class TestGymUserModel:
    def test_create_gym_user(self):
        """Test creating a gym user"""
        user = GymUserFactory(phone="1234567890")
        assert user.phone == "1234567890"
        assert user.is_verified is True
        assert str(user) == "1234567890"

    def test_gym_user_unique_phone(self):
        """Test phone number uniqueness"""
        GymUserFactory(phone="1111111111")
        with pytest.raises(Exception):
            GymUserFactory(phone="1111111111")

    def test_gym_user_default_values(self):
        """Test default values"""
        user = GymUser.objects.create(phone="9999999999")
        assert user.is_verified is False
        assert user.email == ""
        assert user.created_at is not None


@pytest.mark.django_db
class TestOTPModel:
    def test_create_otp(self):
        """Test creating an OTP"""
        otp = OTPFactory(phone="1234567890", otp="123456")
        assert otp.phone == "1234567890"
        assert otp.otp == "123456"
        assert str(otp) == "1234567890 - 123456"

    def test_otp_not_expired(self):
        """Test OTP is not expired immediately"""
        otp = OTPFactory()
        assert otp.is_expired() is False

    def test_otp_expired_after_5_minutes(self):
        """Test OTP expires after 5 minutes"""
        otp = OTPFactory()
        # Manually set created_at to 6 minutes ago
        otp.created_at = timezone.now() - timedelta(minutes=6)
        otp.save()
        assert otp.is_expired() is True

    def test_multiple_otps_same_phone(self):
        """Test multiple OTPs can exist for same phone"""
        phone = "1234567890"
        otp1 = OTPFactory(phone=phone, otp="111111")
        otp2 = OTPFactory(phone=phone, otp="222222")
        assert OTP.objects.filter(phone=phone).count() == 2


@pytest.mark.django_db
class TestProfileModel:
    def test_create_profile(self, gym_user):
        """Test creating a profile"""
        profile = Profile.objects.create(
            user=gym_user,
            name="Test User",
            email="test@example.com",
            height=175.5,
            weight=70.5
        )
        assert profile.user == gym_user
        assert profile.name == "Test User"
        assert str(profile) == "Test User"

    def test_profile_optional_fields(self, gym_user):
        """Test profile with optional fields"""
        profile = Profile.objects.create(
            user=gym_user,
            name="Test User",
            email="test@example.com"
        )
        assert profile.height is None
        assert profile.weight is None
        assert profile.medical_notes == ""
        assert profile.emergency_contact == ""

    def test_profile_one_to_one_relationship(self, gym_user):
        """Test one-to-one relationship"""
        ProfileFactory(user=gym_user)
        with pytest.raises(Exception):
            ProfileFactory(user=gym_user)


@pytest.mark.django_db
class TestBookingModel:
    def test_create_booking(self, gym_user, trainer, program):
        """Test creating a booking"""
        booking = Booking.objects.create(
            user=gym_user,
            user_name="Test User",
            user_phone=gym_user.phone,
            trainer=trainer,
            program=program,
            preferred_date="2026-02-01",
            preferred_time="morning",
            message="Test message"
        )
        assert booking.user == gym_user
        assert booking.trainer == trainer
        assert booking.program == program
        assert booking.preferred_time == "morning"
        assert "Test User" in str(booking)

    def test_booking_without_trainer(self, gym_user, program):
        """Test booking without specifying a trainer"""
        booking = Booking.objects.create(
            user=gym_user,
            user_name="Test User",
            user_phone=gym_user.phone,
            program=program,
            preferred_date="2026-02-01",
            preferred_time="evening"
        )
        assert booking.trainer is None

    def test_booking_time_choices(self, gym_user, program):
        """Test booking time choices"""
        for time_choice in ['morning', 'afternoon', 'evening']:
            booking = BookingFactory(
                user=gym_user,
                program=program,
                preferred_time=time_choice
            )
            assert booking.preferred_time == time_choice

    def test_booking_ordering(self, gym_user, program):
        """Test bookings are ordered by created_at descending"""
        booking1 = BookingFactory(user=gym_user, program=program)
        booking2 = BookingFactory(user=gym_user, program=program)
        bookings = Booking.objects.all()
        assert bookings[0] == booking2
        assert bookings[1] == booking1