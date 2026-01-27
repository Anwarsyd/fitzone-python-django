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