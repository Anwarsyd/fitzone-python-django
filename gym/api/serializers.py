from rest_framework import serializers
from gym.models import (
    Slider, Program, Feature, Specialization,
    Trainer, Faq, Gallery, Testimonial
)


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['id', 'title']


class ProgramSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True, read_only=True)
    
    class Meta:
        model = Program
        fields = [
            'id', 'title', 'description', 'features',
            'thumbnail', 'cover', 'image1', 'image2',
            'duration', 'price'
        ]


class TrainerSerializer(serializers.ModelSerializer):
    certifications = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Trainer
        fields = [
            'id', 'name', 'specialization', 'picture',
            'bio', 'experience', 'certifications',
            'twitter', 'facebook', 'instagram'
        ]


class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ['id', 'caption', 'slogan', 'image']


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ['id', 'question', 'answer']


class GallerySerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Gallery
        fields = ['id', 'title', 'image', 'category', 'category_display']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'program', 'testimonial', 'image', 'rating']