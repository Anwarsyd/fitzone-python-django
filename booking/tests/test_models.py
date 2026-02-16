# booking/tests/test_models.py

import pytest
from django.utils import timezone
from datetime import timedelta
from booking.models import GymUser, OTP, Profile, Booking
from booking.tests.factories import (
    GymUserFactory, SuperuserFactory, OTPFactory,
    ProfileFactory, BookingFactory
)


@pytest.mark.django_db
class TestGymUserModel:

    # ─────────────────────────────────────
    # EXISTING tests — still valid
    # ─────────────────────────────────────
    def test_create_gym_user(self):
        user = GymUserFactory()
        assert user.phone is not None
        assert user.is_verified is True
        assert str(user) == user.phone

    def test_gym_user_unique_phone(self):
        GymUserFactory(phone="1111111111")
        with pytest.raises(Exception):
            GymUserFactory(phone="1111111111")

    # ─────────────────────────────────────
    # NEW: AbstractBaseUser specific tests
    # ─────────────────────────────────────
    def test_create_user_via_manager(self):
        """create_user sets unusable password"""
        user = GymUser.objects.create_user(phone="5555555555")
        assert user.phone == "5555555555"
        assert not user.has_usable_password()   # ← OTP-based

    def test_create_superuser_via_manager(self):
        """create_superuser sets real password and staff flags"""
        admin = GymUser.objects.create_superuser(
            phone="6666666666",
            password="admin123"
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.has_usable_password()      # ← password-based
        assert admin.check_password("admin123") is True

    def test_create_user_without_phone_raises(self):
        """GymUserManager requires phone"""
        with pytest.raises(ValueError):
            GymUser.objects.create_user(phone="")

    def test_create_superuser_without_password_raises(self):
        """Superuser must have a password"""
        with pytest.raises(ValueError, match="Superuser must have a password"):
            GymUser.objects.create_superuser(
                phone="7777777777",
                password=None
            )

    def test_username_field_is_phone(self):
        """USERNAME_FIELD must be phone"""
        assert GymUser.USERNAME_FIELD == 'phone'

    def test_required_fields_is_empty(self):
        """No extra required fields beyond phone"""
        assert GymUser.REQUIRED_FIELDS == []

    def test_member_cannot_login_with_password(self):
        """Regular member has unusable password by design"""
        user = GymUser.objects.create_user(phone="8888888888")
        assert not user.has_usable_password()
        assert not user.check_password("anypassword")

    def test_is_active_default_true(self):
        """New users are active by default"""
        user = GymUser.objects.create_user(phone="3333333333")
        assert user.is_active is True

    def test_is_staff_default_false(self):
        """New users are not staff by default"""
        user = GymUser.objects.create_user(phone="4444444444")
        assert user.is_staff is False

    def test_get_full_name_returns_profile_name(self, db):
        """get_full_name returns profile name when available"""
        user = GymUser.objects.create_user(phone="2222222222")
        Profile.objects.create(
            user=user, name="John Doe", email="john@test.com"
        )
        assert user.get_full_name() == "John Doe"

    def test_get_full_name_returns_phone_without_profile(self):
        """get_full_name falls back to phone when no profile"""
        user = GymUser.objects.create_user(phone="1212121212")
        assert user.get_full_name() == "1212121212"

    def test_gym_user_default_values(self):
        """Test all default field values"""
        user = GymUser.objects.create_user(phone="9999999999")
        assert user.is_verified is False
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.email == ""
        assert user.created_at is not None


@pytest.mark.django_db
class TestOTPModel:

    def test_create_otp(self):
        otp = OTPFactory(phone="1234567890", otp="123456")
        assert otp.phone == "1234567890"
        assert otp.otp == "123456"
        assert str(otp) == "1234567890 - 123456"

    def test_otp_not_expired(self):
        otp = OTPFactory()
        assert otp.is_expired() is False

    def test_otp_expired_after_5_minutes(self):
        otp = OTPFactory()
        otp.created_at = timezone.now() - timedelta(minutes=6)
        otp.save()
        assert otp.is_expired() is True

    def test_otp_boundary_exactly_5_minutes(self):
        """OTP at exactly 5 minutes should be expired"""
        otp = OTPFactory()
        otp.created_at = timezone.now() - timedelta(minutes=5, seconds=1)
        otp.save()
        assert otp.is_expired() is True

    def test_multiple_otps_same_phone(self):
        phone = "1234567890"
        OTPFactory(phone=phone, otp="111111")
        OTPFactory(phone=phone, otp="222222")
        assert OTP.objects.filter(phone=phone).count() == 2


@pytest.mark.django_db
class TestProfileModel:

    def test_create_profile(self, gym_user):
        profile = Profile.objects.create(
            user=gym_user,
            name="Test User",
            email="test@example.com",
            height=175.5,
            weight=70.5
        )
        assert profile.user == gym_user
        assert str(profile) == "Test User"

    # ─────────────────────────────────────
    # NEW: BMI property test
    # ─────────────────────────────────────
    def test_bmi_calculated_correctly(self, gym_user):
        """BMI = weight / height_m^2"""
        profile = Profile.objects.create(
            user=gym_user, name="Test",
            email="t@t.com",
            height=175.0, weight=70.0
        )
        # 70 / (1.75^2) = 22.86
        assert profile.bmi == 22.86

    def test_bmi_returns_none_without_height(self, gym_user):
        profile = Profile.objects.create(
            user=gym_user, name="Test",
            email="t@t.com",
            weight=70.0
        )
        assert profile.bmi is None

    def test_bmi_returns_none_without_weight(self, gym_user):
        profile = Profile.objects.create(
            user=gym_user, name="Test",
            email="t@t.com",
            height=175.0
        )
        assert profile.bmi is None

    def test_profile_one_to_one_relationship(self, gym_user):
        ProfileFactory(user=gym_user)
        with pytest.raises(Exception):
            ProfileFactory(user=gym_user)  # can't have two profiles


@pytest.mark.django_db
class TestBookingModel:

    def test_create_booking(self, gym_user, trainer, program):
        booking = Booking.objects.create(
            user=gym_user,
            user_name="Test User",
            user_phone=gym_user.phone,
            trainer=trainer,
            program=program,
            preferred_date="2026-06-01",
            preferred_time="morning",
        )
        assert booking.user == gym_user
        assert "Test User" in str(booking)

    def test_booking_without_trainer(self, gym_user, program):
        booking = Booking.objects.create(
            user=gym_user,
            user_name="Test User",
            user_phone=gym_user.phone,
            program=program,
            preferred_date="2026-06-01",
            preferred_time="evening"
        )
        assert booking.trainer is None

    def test_booking_ordering_latest_first(self, gym_user, program):
        b1 = BookingFactory(user=gym_user, program=program)
        b2 = BookingFactory(user=gym_user, program=program)
        bookings = Booking.objects.all()
        assert bookings[0] == b2   # newest first
        assert bookings[1] == b1