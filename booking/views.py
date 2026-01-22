from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .models import GymUser, OTP, Booking, Profile
from gym.models import Trainer, Program
import random

from django.conf import settings
from django.core.mail import send_mail


# otp send 
class SendOTPView(View):
    def get(self, request):
        return render(request, "booking/send_otp.html")

    def post(self, request):
        phone = request.POST.get("phone")

        user, _ = GymUser.objects.get_or_create(phone=phone)

        otp = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, otp=otp)

        print(f"OTP for {phone}: {otp}")  # Demo only

        request.session["otp_phone"] = phone
        messages.success(request, "OTP sent successfully")
        return redirect("Booking:verify_otp")


# otp verify 
class VerifyOTPView(View):
    def get(self, request):
        return render(request, "booking/verify_otp.html")

    def post(self, request):
        phone = request.session.get("otp_phone")
        entered_otp = request.POST.get("otp")

        otp_obj = OTP.objects.filter(phone=phone).last()

        if not otp_obj:
            messages.error(request, "OTP not found")
            return redirect("Booking:send_otp")

        if otp_obj.is_expired():
            messages.error(request, "OTP expired. Please try again.")
            return redirect("Booking:send_otp")

        if otp_obj.otp != entered_otp:
            messages.error(request, "Invalid OTP")
            return redirect("Booking:verify_otp")

        user = GymUser.objects.get(phone=phone)
        user.is_verified = True
        user.save()

        request.session["user_id"] = user.id
        del request.session["otp_phone"]

        messages.success(request, "Login successful")
        return redirect("Booking:booking")


class BookingView(View):
    template_name = "booking/index.html"

    def get(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            messages.info(request, "Please login using your mobile number.")
            return redirect("Booking:send_otp")

        user = GymUser.objects.get(id=user_id)
        
        # Get profile if exists
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        context = {
            "user": user,
            "profile": profile,
            "trainers": Trainer.objects.all(),
            "programs": Program.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            messages.error(request, "Please login using your mobile number.")
            return redirect("Booking:send_otp")

        user = GymUser.objects.get(id=user_id)

        # Get form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        program_id = request.POST.get("program")
        trainer_id = request.POST.get("trainer")
        date = request.POST.get("date")
        time = request.POST.get("time")
        message = request.POST.get("message", "")

        if not all([name, email, program_id, date, time]):
            messages.error(request, "Please fill all required fields.")
            return redirect("Booking:booking")

        # Update or create profile with name and email
        profile, created = Profile.objects.get_or_create(user=user)
        profile.name = name
        profile.email = email
        profile.save()

        # Update user email
        user.email = email
        user.save()

        # Fetch program and trainer objects
        program = Program.objects.get(id=program_id)
        trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None

        # Create booking with snapshot data
        booking = Booking.objects.create(
            user=user,
            user_name=name,
            user_phone=user.phone,
            program=program,
            trainer=trainer,
            preferred_date=date,
            preferred_time=time,
            message=message
        )

        # Send confirmation email
        if email:
            try:
                trainer_name = trainer.name if trainer else "our team"
                send_mail(
                    subject='FitZone - Booking Confirmation',
                    message=f"""Dear {name},

                    Your class booking for {program.title} with {trainer_name} on {date} ({time}) has been confirmed.

                    See you at the gym!

                    FitZone Team
                    """,
                    from_email='noreply@fitzone.com',
                    recipient_list=[email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email not sent: {e}")

        messages.success(request, "Your class has been booked successfully! Check your email for confirmation.")
        return redirect("gym:index")


# Profile View
class ProfileView(View):
    template_name = "booking/profile.html"

    def get(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            messages.info(request, "Please login to view your profile.")
            return redirect("Booking:send_otp")

        user = GymUser.objects.get(id=user_id)
        
        # Get or create profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'name': '',
                'email': user.email or ''
            }
        )

        # Get user's bookings
        bookings = Booking.objects.filter(user=user)

        context = {
            "user": user,
            "profile": profile,
            "bookings": bookings,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            messages.error(request, "Please login to update your profile.")
            return redirect("Booking:send_otp")

        user = GymUser.objects.get(id=user_id)
        profile, created = Profile.objects.get_or_create(user=user)

        # Update profile fields
        profile.name = request.POST.get("name", "")
        profile.email = request.POST.get("email", "")
        profile.height = request.POST.get("height") or None
        profile.weight = request.POST.get("weight") or None
        profile.emergency_contact = request.POST.get("emergency_contact", "")
        profile.medical_notes = request.POST.get("medical_notes", "")

        # Handle profile photo upload
        if request.FILES.get("profile_photo"):
            profile.profile_photo = request.FILES["profile_photo"]

        profile.save()

        # Also update email in GymUser if provided
        if profile.email:
            user.email = profile.email
            user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("Booking:profile")


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect("Booking:send_otp")