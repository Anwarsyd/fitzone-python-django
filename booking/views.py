from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .models import Booking
from gym.models import Trainer,Program
from django.core.mail import send_mail
from django.contrib import messages
# Create your views here.
class BookingView(TemplateView):
    template_name="booking/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trainers'] = Trainer.objects.all()
        context['programs'] = Program.objects.all()
        return context
    
    def post(self,request,*args,**kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        trainer_id = request.POST.get('trainer')
        program_id = request.POST.get('program')
        date = request.POST.get('date')
        time = request.POST.get('time')
        message = request.POST.get('message', '')
        
        if all([name,phone,program_id,date,time]):
            program = Program.objects.get(id=program_id)
            trainer = Trainer.objects.get(id=trainer_id) if trainer_id else None
            
            booking = Booking.objects.create(
                name=name,
                email=email,
                phone=phone,
                trainer=trainer,
                program=program,
                preferred_date=date,
                preferred_time=time,
                message=message
            )
            # Send confirmation email
            try:
                trainer_name = trainer.name if trainer else "our team"
                send_mail(
                    'FitZone - Booking Confirmation',
                    f'Dear {name},\n\nYour class booking for {program.title} with {trainer_name} on {date} ({time}) has been confirmed.\n\nSee you at the gym!\n\nFitZone Team',
                    'noreply@fitzone.com',
                    [email],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, 'Your class has been booked successfully! Check your email for confirmation.')
            return redirect('Booking:booking')
        
        messages.error(request, 'Please fill all required fields.')
        return redirect('Booking:booking')
        
        