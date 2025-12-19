from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.contrib import messages

from .models import GymUser, OTP, Booking
from gym.models import Trainer,Program
import random

# otp send 
def send_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")

        user, created = GymUser.objects.get_or_create(phone=phone)

        otp = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, otp=otp)

        # TODO: integrate SMS API
        print(f"Demo OTP for {phone} is: {otp}")

        request.session["phone"] = phone
        return redirect("Booking:verify_otp")

    return render(request, "booking/send_otp.html")

# otp verify 
def verify_otp(request):
    phone = request.session.get("phone")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        otp_obj = OTP.objects.filter(phone=phone).last()

        if otp_obj and otp_obj.otp == entered_otp:
            user = GymUser.objects.get(phone=phone)
            user.is_verified = True
            user.save()

            request.session["user_id"] = user.id
            messages.success(request, "Login successful!")
            return redirect("Booking:booking")

        messages.error(request, "Invalid OTP")

    return render(request, "booking/verify_otp.html")



class BookingView(TemplateView):
    template_name="booking/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainers'] = Trainer.objects.all()
        context['programs'] = Program.objects.all()
        return context
    
    def post(self,request,*args,**kwargs):
        
        user_id = request.session.get("user_id")
        if not user_id:
            messages.error(request, "Please login using mobile number.")
            return redirect("Booking:send_otp")

        user = GymUser.objects.get(id=user_id)

        trainer_id = request.POST.get('trainer')
        program_id = request.POST.get('program')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message', '')
        
        if all([program_id,date,time]):
            program = Program.objects.get(id=program_id)
            trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None
            
            booking = Booking.objects.create(
                user=user,
                trainer=trainer,
                program=program,
                preferred_date=date,
                preferred_time=time,
                message=message
            )
            # Send confirmation email
            if user.email:
                try:
                    trainer_name = trainer.name if trainer else "our team"
                    send_mail(
                        'FitZone - Booking Confirmation',
                        f'Dear {user.name},\n\nYour class booking for {program.title} with {trainer_name} on {date} ({time}) has been confirmed.\n\nSee you at the gym!\n\nFitZone Team',
                        'noreply@fitzone.com',
                        [user.email],
                        fail_silently=True,
                    )
                except:
                    pass
            
            messages.success(request, 'Your class has been booked successfully! Check your email for confirmation.')
            return redirect('Booking:booking')
        
        messages.error(request, 'Please fill all required fields.')
        return redirect('Booking:booking')
        
        