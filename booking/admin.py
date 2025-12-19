from django.contrib import admin

# Register your models here.
from .models import Booking,GymUser,OTP

class GymUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'name', 'email', 'is_verified', 'created_at')
    search_fields = ('phone', 'name', 'email')
    
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'otp', 'created_at')
    search_fields = ('phone',)
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'program', 'trainer', 'preferred_date', 'preferred_time', 'created_at']
    list_filter = ['preferred_date', 'preferred_time', 'program', 'trainer']
    search_fields = ['user__phone','user__name','user__email']
    date_hierarchy = 'preferred_date'