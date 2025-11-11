from django.shortcuts import render,redirect
from .models import Slider, Program, Trainer, Faq, Gallery, Testimonial
from django.views.generic import ListView,DetailView,TemplateView
from django.core.mail import send_mail
# Create your views here.

class HomeView(ListView):
    template_name = "gym/index.html"
    queryset = Program.objects.all()
    context_object_name = 'programs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sliders"] = Slider.objects.all()
        context['trainers'] = Trainer.objects.all()
        context['testimonials'] = Testimonial.objects.all()[:3]
        return context

class ProgramListView(ListView):
    template_name = 'gym/programs.html'
    queryset = Program.objects.all()
    context_object_name="programs_list"
    

class ProgramDetailsView(DetailView):
    template_name = 'gym/program_details.html'
    queryset = Program.objects.all()
    context_object_name = 'program_details'
    
class FaqsView(ListView):
    template_name="gym/faqs.html"
    queryset=Faq.objects.all()
    
class TrainersView(ListView):
    template_name = "gym/trainers.html"
    queryset = Trainer.objects.all()
    
class TrainerDetailsView(DetailView):
    template_name = "gym/trainer_details.html"
    queryset = Trainer.objects.all()
    
class GalleryListView(ListView):
    template_name = 'gym/gallery.html'
    queryset = Gallery.objects.all()
    paginate_by = 9
    
class ContactView(TemplateView):
    template_name = "gym/contact.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject', 'FitZone Inquiry')
        message = request.POST.get('message')

        if name and message and email and phone:
            try:
                send_mail(
                    f"{subject} - {phone}",
                    f"From: {name}\nEmail: {email}\n\n{message}",
                    email,
                    ['your-email@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Message sent successfully!")
            except:
                messages.error(request, "Failed to send message.")

        return redirect('contact')