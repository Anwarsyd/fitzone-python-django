from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GymUser, OTP, Booking, Profile

@admin.register(GymUser)
class GymUserAdmin(UserAdmin):
    model        = GymUser
    list_display = ('phone', 'email', 'is_verified', 'is_staff', 'created_at')
    list_filter  = ('is_verified', 'is_staff', 'is_active')
    search_fields = ('phone', 'email')
    ordering     = ('-created_at',)

    # Fields shown when EDITING a user
    fieldsets = (
        (None,          {'fields': ('phone', 'password')}),
        ('Personal',    {'fields': ('email',)}),
        ('Status',      {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Dates',       {'fields': ('last_login',)}),
    )

    # Fields shown when CREATING a user in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2', 'is_staff'),
        }),
    )

    
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
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'user', 'height', 'weight', 'updated_at')
    search_fields = ('name', 'email', 'user__phone')