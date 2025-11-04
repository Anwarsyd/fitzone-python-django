from django.shortcuts import render,redirect
from .models import Slider, Program, Trainer, Faq, Gallery, Testimonial
from django.views.generic import ListView,DetailView
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