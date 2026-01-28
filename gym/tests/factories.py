import factory
from factory.django import DjangoModelFactory, ImageField
from gym.models import (
    Slider, Program, Feature, Specialization,
    Trainer, Faq, Gallery, Testimonial
)
from faker import Faker

fake = Faker()


class SliderFactory(DjangoModelFactory):
    class Meta:
        model = Slider

    caption = factory.LazyAttribute(lambda _: fake.catch_phrase())
    slogan = factory.LazyAttribute(lambda _: fake.sentence())
    image = ImageField()


class FeatureFactory(DjangoModelFactory):
    class Meta:
        model = Feature

    title = factory.LazyAttribute(lambda _: fake.word().title())


class ProgramFactory(DjangoModelFactory):
    class Meta:
        model = Program

    title = factory.LazyAttribute(lambda _: fake.catch_phrase())
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=200))
    thumbnail = ImageField()
    cover = ImageField()
    duration = factory.Iterator(["3 months", "6 months", "1 year"])
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)

    @factory.post_generation
    def features(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for feature in extracted:
                self.features.add(feature)


class SpecializationFactory(DjangoModelFactory):
    class Meta:
        model = Specialization

    name = factory.LazyAttribute(lambda _: fake.job())


class TrainerFactory(DjangoModelFactory):
    class Meta:
        model = Trainer

    name = factory.LazyAttribute(lambda _: fake.name())
    specialization = factory.LazyAttribute(lambda _: fake.job())
    picture = ImageField()
    bio = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=200))
    experience = factory.LazyAttribute(lambda _: f"{fake.random_int(min=1, max=20)} years")
    twitter = factory.LazyAttribute(lambda _: f"@{fake.user_name()}")
    facebook = factory.LazyAttribute(lambda _: fake.user_name())
    instagram = factory.LazyAttribute(lambda _: f"@{fake.user_name()}")

    @factory.post_generation
    def certifications(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for cert in extracted:
                self.certifications.add(cert)


class FaqFactory(DjangoModelFactory):
    class Meta:
        model = Faq

    question = factory.LazyAttribute(lambda _: fake.sentence(nb_words=8).rstrip('.') + '?')
    answer = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=150))


class GalleryFactory(DjangoModelFactory):
    class Meta:
        model = Gallery

    title = factory.LazyAttribute(lambda _: fake.catch_phrase())
    image = ImageField()
    category = factory.Iterator(['gym', 'classes', 'facility', 'events'])


class TestimonialFactory(DjangoModelFactory):
    class Meta:
        model = Testimonial

    name = factory.LazyAttribute(lambda _: fake.name())
    program = factory.LazyAttribute(lambda _: fake.catch_phrase())
    testimonial = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=150))
    image = ImageField()
    rating = factory.Iterator([3, 4, 5])