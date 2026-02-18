from rest_framework import serializers
from booking.models import GymUser, Profile, Booking, OTP
from gym.api.serializers import ProgramSerializer, TrainerSerializer
from django.utils import timezone
import random


class GymUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymUser
        fields = ['id', 'phone', 'email', 'is_verified', 'created_at']
        read_only_fields = ['is_verified', 'created_at']


class ProfileSerializer(serializers.ModelSerializer):
    bmi = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'name', 'email', 'profile_photo',
            'height', 'weight', 'bmi', 'medical_notes',
            'emergency_contact', 'updated_at'
        ]
        read_only_fields = ['user', 'updated_at']
    
    def get_bmi(self, obj):
        if obj.height and obj.weight:
            height_m = float(obj.height) / 100
            bmi = float(obj.weight) / (height_m ** 2)
            return round(bmi, 2)
        return None


class BookingSerializer(serializers.ModelSerializer):
    program_details = ProgramSerializer(source='program', read_only=True)
    trainer_details = TrainerSerializer(source='trainer', read_only=True)
    time_display = serializers.CharField(source='get_preferred_time_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'user_name', 'user_phone',
            'program', 'program_details', 'trainer', 'trainer_details',
            'preferred_date', 'preferred_time', 'time_display',
            'message', 'created_at'
        ]
        read_only_fields = ['user', 'user_phone', 'created_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user.gymuser
        
        validated_data['user'] = user
        validated_data['user_phone'] = user.phone
        
        return super().create(validated_data)


class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    
    def validate_phone(self, value):
        # Remove non-digits
        cleaned = ''.join(filter(str.isdigit, value))
        
        # Check it's reasonable length
        if len(cleaned) < 10:
            raise serializers.ValidationError("Phone number too short")
        
        # Store the cleaned version
        return cleaned


class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=6)
    
    def validate(self, data):
        phone = data.get('phone')
        otp = data.get('otp')
        
        try:
            otp_obj = OTP.objects.filter(phone=phone).latest('created_at')
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")
        
        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP expired")
        
        if otp_obj.otp != otp:
            raise serializers.ValidationError("Invalid OTP")
        
        user, created = GymUser.objects.get_or_create(phone=phone)
        user.is_verified = True
        user.save()
        
        data['user'] = user
        return data