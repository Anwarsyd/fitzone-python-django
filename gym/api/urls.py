from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SliderViewSet, ProgramViewSet, TrainerViewSet,
    FaqViewSet, GalleryViewSet, TestimonialViewSet
)

router = DefaultRouter()
router.register(r'sliders', SliderViewSet, basename='slider')
router.register(r'programs', ProgramViewSet, basename='program')
router.register(r'trainers', TrainerViewSet, basename='trainer')
router.register(r'faqs', FaqViewSet, basename='faq')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('', include(router.urls)),
]