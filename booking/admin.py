from django.contrib import admin

# Register your models here.
from .models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'trainer', 'preferred_date', 'preferred_time', 'created_at']
    list_filter = ['preferred_date', 'preferred_time', 'program', 'trainer']
    search_fields = ['name', 'email', 'phone']
    date_hierarchy = 'preferred_date'