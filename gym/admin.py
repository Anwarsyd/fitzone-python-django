from django.contrib import admin
from .models import Slider, Program, Feature, Trainer, Specialization, Faq, Gallery, Testimonial
# Register your models here.

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['caption','slogan']
    
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'price']
    filter_horizontal = ['features']
    
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization']
    filter_horizontal = ['certifications']
    
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['question']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']
    list_filter = ['category']
    
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'rating']