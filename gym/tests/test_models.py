import pytest
from gym.models import (
    Slider, Program, Feature, Specialization,
    Trainer, Faq, Gallery, Testimonial
)
from gym.tests.factories import (
    SliderFactory, ProgramFactory, FeatureFactory,
    SpecializationFactory, TrainerFactory, FaqFactory,
    GalleryFactory, TestimonialFactory
)


@pytest.mark.django_db
class TestSliderModel:
    def test_create_slider(self, slider):
        """Test creating a slider"""
        assert slider.caption == "Get Fit Today"
        assert slider.slogan is not None
        assert slider.image is not None
        assert "Get Fit Today" in str(slider)

    def test_slider_str_truncation(self, slider):
        """Test slider string representation truncates at 20 chars"""
        slider.caption = "A" * 50
        slider.save()
        assert len(str(slider)) <= 20

    def test_slider_verbose_name_plural(self):
        """Test verbose name plural"""
        assert Slider._meta.verbose_name_plural == 'Sliders'


@pytest.mark.django_db
class TestFeatureModel:
    def test_create_feature(self, feature):
        """Test creating a feature"""
        assert feature.title == "Personal Training"
        assert str(feature) == "Personal Training"

    def test_feature_in_program(self, program, feature):
        """Test feature can be associated with program"""
        assert feature in program.features.all()


@pytest.mark.django_db
class TestProgramModel:
    def test_create_program(self, program):
        """Test creating a program"""
        assert program.title == "Weight Loss Program"
        assert program.description is not None
        assert program.duration == "3 months"
        assert program.price == 299.99
        assert str(program) == "Weight Loss Program"

    def test_program_optional_fields(self, test_image):
        """Test program with optional fields"""
        program = Program.objects.create(
            title="Basic Program",
            description="Test description",
            thumbnail=test_image,
            cover=test_image,
            duration="1 month"
        )
        assert program.price is None
        assert program.image1.name == ''
        assert program.image2.name == ''

    def test_program_many_to_many_features(self, program):
        """Test program can have multiple features"""
        feature1 = FeatureFactory(title="Feature 1")
        feature2 = FeatureFactory(title="Feature 2")
        program.features.add(feature1, feature2)
        assert program.features.count() >= 2


@pytest.mark.django_db
class TestSpecializationModel:
    def test_create_specialization(self, specialization):
        """Test creating a specialization"""
        assert specialization.name == "Strength Training"
        assert str(specialization) == "Strength Training"

    def test_specialization_verbose_name_plural(self):
        """Test verbose name plural"""
        assert Specialization._meta.verbose_name_plural == 'Specializations'


@pytest.mark.django_db
class TestTrainerModel:
    def test_create_trainer(self, trainer):
        """Test creating a trainer"""
        assert trainer.name == "John Doe"
        assert trainer.specialization == "Strength Training"
        assert trainer.bio == "Experienced fitness trainer"
        assert str(trainer) == "John Doe"

    def test_trainer_social_media(self, trainer):
        """Test trainer social media fields"""
        assert trainer.twitter == "@johndoe"
        assert trainer.facebook == "johndoe"
        assert trainer.instagram == "@johndoe"

    def test_trainer_certifications(self, trainer, specialization):
        """Test trainer certifications relationship"""
        assert specialization in trainer.certifications.all()

    def test_trainer_optional_social_media(self, test_image):
        """Test trainer without social media"""
        trainer = Trainer.objects.create(
            name="Jane Doe",
            specialization="Yoga",
            picture=test_image,
            bio="Yoga expert",
            experience="5 years"
        )
        assert trainer.twitter is None or trainer.twitter == ""
        assert trainer.facebook is None or trainer.facebook == ""


@pytest.mark.django_db
class TestFaqModel:
    def test_create_faq(self, faq):
        """Test creating a FAQ"""
        assert faq.question == "What are your opening hours?"
        assert faq.answer == "We are open 24/7 for our members"
        assert str(faq) == "What are your opening hours?"

    def test_multiple_faqs(self):
        """Test creating multiple FAQs"""
        faq1 = FaqFactory(question="Question 1?")
        faq2 = FaqFactory(question="Question 2?")
        assert Faq.objects.count() == 2


@pytest.mark.django_db
class TestGalleryModel:
    def test_create_gallery(self, gallery):
        """Test creating a gallery item"""
        assert gallery.title == "Modern Gym Equipment"
        assert gallery.category == "gym"
        assert str(gallery) == "Modern Gym Equipment"

    def test_gallery_categories(self, test_image):
        """Test different gallery categories"""
        categories = ['gym', 'classes', 'facility', 'events']
        for category in categories:
            gallery = Gallery.objects.create(
                title=f"Test {category}",
                image=test_image,
                category=category
            )
            assert gallery.category == category

    def test_gallery_default_category(self, test_image):
        """Test default category"""
        gallery = Gallery.objects.create(
            title="Test Gallery",
            image=test_image
        )
        assert gallery.category == 'facility'

    def test_gallery_verbose_name_plural(self):
        """Test verbose name plural"""
        assert Gallery._meta.verbose_name_plural == 'Galleries'


@pytest.mark.django_db
class TestTestimonialModel:
    def test_create_testimonial(self, testimonial):
        """Test creating a testimonial"""
        assert testimonial.name == "Jane Smith"
        assert testimonial.program == "Weight Loss Program"
        assert testimonial.rating == 5
        assert "Jane Smith" in str(testimonial)
        assert "Weight Loss Program" in str(testimonial)

    def test_testimonial_rating_choices(self, test_image):
        """Test rating choices"""
        for rating in range(1, 6):
            testimonial = Testimonial.objects.create(
                name=f"User {rating}",
                program="Test Program",
                testimonial="Great program!",
                image=test_image,
                rating=rating
            )
            assert testimonial.rating == rating

    def test_testimonial_default_rating(self, test_image):
        """Test default rating"""
        testimonial = Testimonial.objects.create(
            name="Test User",
            program="Test Program",
            testimonial="Good experience",
            image=test_image
        )
        assert testimonial.rating == 5