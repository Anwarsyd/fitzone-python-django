from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages
from .models import GymUser, OTP, Booking
from gym.models import Trainer,Program
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

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail
from .models import GymUser, Booking
from gym.models import Trainer, Program

class BookingView(View):
    template_name = "booking/index.html"

    def get(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            messages.info(request, "Please login using your mobile number.")
            return redirect("Booking:send_otp")

        user = GymUser.objects.get(id=user_id)

        context = {
            "user": user,  # For read-only phone
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
        program_id = request.POST.get("program")
        trainer_id = request.POST.get("trainer")
        date = request.POST.get("date")
        time = request.POST.get("time")
        message = request.POST.get("message", "")

        if not all([program_id, date, time]):
            messages.error(request, "Please fill all required fields.")
            return redirect("Booking:booking")

        # Fetch program and trainer objects
        program = Program.objects.get(id=program_id)
        trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None

        # Create booking
        booking = Booking.objects.create(
            user=user,
            program=program,
            trainer=trainer,
            preferred_date=date,
            preferred_time=time,
            message=message
        )

        # Send confirmation email
        if user.email:
            try:
                trainer_name = trainer.name if trainer else "our team"
                send_mail(
                    subject='FitZone - Booking Confirmation',
                    message=f"""Dear {user.name or user.phone},

                    Your class booking for {program.title} with {trainer_name} on {date} ({time}) has been confirmed.

                    See you at the gym!

                    FitZone Team
                    """,
                    
                    from_email='noreply@fitzone.com',
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email not sent: {e}")

        messages.success(request, "Your class has been booked successfully! Check your email for confirmation.")
        return redirect("Booking:booking")


def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect("Booking:send_otp")

        
