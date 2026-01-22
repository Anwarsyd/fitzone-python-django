from django.db import models
from gym.models import Trainer, Program
from django.utils import timezone
from datetime import timedelta


# Auth user - OTP based
class GymUser(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
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

    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)

    # snapshot
    user_name = models.CharField(max_length=120)
    user_phone = models.CharField(max_length=20)

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)
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