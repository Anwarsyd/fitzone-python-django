from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from gym.models import (
    Slider, Program, Trainer, Faq, Gallery, Testimonial
)
from .serializers import (
    SliderSerializer, ProgramSerializer, TrainerSerializer,
    FaqSerializer, GallerySerializer, TestimonialSerializer
)


class SliderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [AllowAny]


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'title']


class TrainerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'specialization']


class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]


class GalleryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [AllowAny]
    filterset_fields = ['category']


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]
    ordering = ['-rating']