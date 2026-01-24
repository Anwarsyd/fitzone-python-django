import factory
from factory.django import DjangoModelFactory
from booking.models import GymUser, OTP, Profile, Booking
from gym.models import Trainer, Program
from faker import Faker

fake = Faker()


class GymUserFactory(DjangoModelFactory):
    class Meta:
        model = GymUser

    phone = factory.Sequence(lambda n: f"{1000000000 + n}")
    email = factory.LazyAttribute(lambda _: fake.email())
    is_verified = True


class OTPFactory(DjangoModelFactory):
    class Meta:
        model = OTP

    phone = factory.Sequence(lambda n: f"{1000000000 + n}")
    otp = factory.Sequence(lambda n: f"{100000 + n % 900000}")


class TrainerFactory(DjangoModelFactory):
    class Meta:
        model = Trainer

    name = factory.LazyAttribute(lambda _: fake.name())
    specialization = factory.LazyAttribute(lambda _: fake.job())
    experience = factory.Faker('random_int', min=1, max=20)


class ProgramFactory(DjangoModelFactory):
    class Meta:
        model = Program

    title = factory.LazyAttribute(lambda _: fake.catch_phrase())
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=200))


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(GymUserFactory)
    name = factory.LazyAttribute(lambda _: fake.name())
    email = factory.LazyAttribute(lambda _: fake.email())
    height = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True, min_value=150, max_value=200)
    weight = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True, min_value=50, max_value=120)
    emergency_contact = factory.Sequence(lambda n: f"{9000000000 + n}")


class BookingFactory(DjangoModelFactory):
    class Meta:
        model = Booking

    user = factory.SubFactory(GymUserFactory)
    user_name = factory.LazyAttribute(lambda _: fake.name())
    user_phone = factory.Sequence(lambda n: f"{1000000000 + n}")
    trainer = factory.SubFactory(TrainerFactory)
    program = factory.SubFactory(ProgramFactory)
    preferred_date = factory.Faker('future_date', end_date='+30d')
    preferred_time = factory.Iterator(['morning', 'afternoon', 'evening'])
    message = factory.LazyAttribute(lambda _: fake.sentence())