from django.db import models

# Create your models here.
from gym.models import Trainer,Program

class Booking(models.Model):
    TIME_CHOICES = (
        ('morning', 'Morning (6AM - 12PM)'),
        ('afternoon', 'Afternoon (12PM - 6PM)'),
        ('evening', 'Evening (6PM - 10PM)'),
    )
    
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    trainer = models.ForeignKey(Trainer,on_delete=models.CASCADE,null=True,blank=True)
    program = models.ForeignKey(Program,on_delete=models.CASCADE)
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=10,choices=TIME_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.program.title} - {self.preferred_date}"
    
    class Meta:
        ordering = ['-created_at']