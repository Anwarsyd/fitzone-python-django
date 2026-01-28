import pytest
from django.test import Client
from gym.models import (
    Slider, Program, Feature, Specialization, 
    Trainer, Faq, Gallery, Testimonial
)
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def client():
    """Django test client"""
    return Client()


@pytest.fixture
def test_image():
    """Create a simple test image"""
    from PIL import Image
    import io
    
    image = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=img_io.read(),
        content_type='image/jpeg'
    )


@pytest.fixture
def slider(db, test_image):
    """Create a slider instance"""
    slider = Slider.objects.create(
        caption="Get Fit Today",
        slogan="Transform Your Body, Transform Your Life",
        image=test_image
    )
    return slider


@pytest.fixture
def feature(db):
    """Create a feature instance"""
    feature = Feature.objects.create(
        title="Personal Training"
    )
    return feature


@pytest.fixture
def program(db, test_image, feature):
    """Create a program instance"""
    program = Program.objects.create(
        title="Weight Loss Program",
        description="Comprehensive weight loss program",
        thumbnail=test_image,
        cover=test_image,
        duration="3 months",
        price=299.99
    )
    program.features.add(feature)
    return program


@pytest.fixture
def specialization(db):
    """Create a specialization instance"""
    specialization = Specialization.objects.create(
        name="Strength Training"
    )
    return specialization


@pytest.fixture
def trainer(db, test_image, specialization):
    """Create a trainer instance"""
    trainer = Trainer.objects.create(
        name="John Doe",
        specialization="Strength Training",
        picture=test_image,
        bio="Experienced fitness trainer",
        experience="10 years of professional training",
        twitter="@johndoe",
        facebook="johndoe",
        instagram="@johndoe"
    )
    trainer.certifications.add(specialization)
    return trainer


@pytest.fixture
def faq(db):
    """Create a FAQ instance"""
    faq = Faq.objects.create(
        question="What are your opening hours?",
        answer="We are open 24/7 for our members"
    )
    return faq


@pytest.fixture
def gallery(db, test_image):
    """Create a gallery instance"""
    gallery = Gallery.objects.create(
        title="Modern Gym Equipment",
        image=test_image,
        category="gym"
    )
    return gallery


@pytest.fixture
def testimonial(db, test_image):
    """Create a testimonial instance"""
    testimonial = Testimonial.objects.create(
        name="Jane Smith",
        program="Weight Loss Program",
        testimonial="Amazing results in just 3 months!",
        image=test_image,
        rating=5
    )
    return testimonial