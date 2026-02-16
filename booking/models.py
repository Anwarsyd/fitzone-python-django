from django.db import models
from gym.models import Trainer, Program
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class GymUserManager(BaseUserManager):
    """
    Custom manager for GymUser.
    Phone number is the unique identifier — no username, no email required.
    """

    def create_user(self, phone, email=None, password=None):
        """Create a regular gym member."""
        if not phone:
            raise ValueError('A phone number is required')

        user = self.model(
            phone=phone,
            email=self.normalize_email(email) if email else ''
        )
        # OTP-based — members don't use passwords
        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email=None, password=None):
        """Create an admin user who can log into /admin."""
        if not password:
            raise ValueError('Superuser must have a password')

        user = self.create_user(phone, email)
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.set_password(password)   # admin needs real password
        user.save(using=self._db)
        return user
    


# Auth user - OTP based
class GymUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    Phone number replaces username as the unique identifier.
    Authentication is OTP-based for members, password-based for admins.
    """
    
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Tell Django: "phone is the login field"
    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = []          # nothing extra for createsuperuser
    
    objects = GymUserManager()

    class Meta:
        verbose_name        = 'Gym User'
        verbose_name_plural = 'Gym Users'
        ordering            = ['-created_at']

    def __str__(self):
        return self.phone

    def get_full_name(self):
        try:
            return self.profile.name
        except Profile.DoesNotExist:
            return self.phone

    def get_short_name(self):
        return self.phone
    
# OTP
class OTP(models.Model):
    phone = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone} - {self.otp}"


class Booking(models.Model):
    TIME_CHOICES = (
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening'),
    )

    user = models.ForeignKey(GymUser, on_delete=models.CASCADE,related_name='bookings')

    # snapshot
    user_name = models.CharField(max_length=120)
    user_phone = models.CharField(max_length=20)

    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=10, choices=TIME_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.program.title} - {self.preferred_date}"

    class Meta:
        ordering = ['-created_at']


class Profile(models.Model):
    user = models.OneToOneField(GymUser, on_delete=models.CASCADE)

    name = models.CharField(max_length=120)
    email = models.EmailField()
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    medical_notes = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def bmi(self):
        """Calculate BMI if height and weight are available."""
        if self.height and self.weight:
            height_m = float(self.height) / 100
            return round(float(self.weight) / (height_m ** 2), 2)
        return None