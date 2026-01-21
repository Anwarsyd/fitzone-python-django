from django.db import models
from gym.models import Trainer,Program

from django.utils import timezone
from datetime import timedelta


# User mobile-based
class GymUser(models.Model):
    phone = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120, blank=True)
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
        ('morning', 'Morning (6AM - 12PM)'),
        ('afternoon', 'Afternoon (12PM - 6PM)'),
        ('evening', 'Evening (6PM - 10PM)'),
    )
    
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True,blank=True)
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=10,choices=TIME_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.phone} - {self.program.title} - {self.preferred_date}"
    
    class Meta:
        ordering = ['-created_at']