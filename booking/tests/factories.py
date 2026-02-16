# booking/tests/factories.py

import factory
from factory.django import DjangoModelFactory
from booking.models import GymUser, OTP, Profile, Booking
from gym.models import Trainer, Program
from faker import Faker

fake = Faker()


# ─────────────────────────────────────────
# CHANGED: use _create with create_user()
# so set_unusable_password() is called
# ─────────────────────────────────────────
class GymUserFactory(DjangoModelFactory):
    class Meta:
        model = GymUser

    phone = factory.Sequence(lambda n: f"{1000000000 + n}")
    email = factory.LazyAttribute(lambda _: fake.email())

    # Override _create to use the manager method
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        phone = kwargs.pop('phone')
        email = kwargs.pop('email', None)
        kwargs.pop('is_verified', None)  # handled separately

        user = GymUser.objects.create_user(
            phone=phone,
            email=email,
        )
        user.is_verified = True
        user.save()
        return user


# ─────────────────────────────────────────
# NEW: SuperuserFactory
# ─────────────────────────────────────────
class SuperuserFactory(DjangoModelFactory):
    class Meta:
        model = GymUser

    phone = factory.Sequence(lambda n: f"{9000000000 + n}")
    email = factory.LazyAttribute(lambda _: fake.email())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        phone = kwargs.pop('phone')
        email = kwargs.pop('email', None)

        return GymUser.objects.create_superuser(
            phone=phone,
            email=email,
            password='testpass123'
        )


class OTPFactory(DjangoModelFactory):
    class Meta:
        model = OTP

    phone = factory.Sequence(lambda n: f"{1000000000 + n}")
    otp   = factory.Sequence(lambda n: f"{100000 + n % 900000}")


class TrainerFactory(DjangoModelFactory):
    class Meta:
        model = Trainer

    name           = factory.LazyAttribute(lambda _: fake.name())
    specialization = factory.LazyAttribute(lambda _: fake.job())
    experience     = factory.Faker('random_int', min=1, max=20)


class ProgramFactory(DjangoModelFactory):
    class Meta:
        model = Program

    title       = factory.LazyAttribute(lambda _: fake.catch_phrase())
    description = factory.LazyAttribute(lambda _: fake.text(max_nb_chars=200))
    duration    = factory.Iterator(["3 months", "6 months", "1 year"])


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user              = factory.SubFactory(GymUserFactory)
    name              = factory.LazyAttribute(lambda _: fake.name())
    email             = factory.LazyAttribute(lambda _: fake.email())
    height            = factory.Faker('pydecimal', left_digits=3, right_digits=2,
                                      positive=True, min_value=150, max_value=200)
    weight            = factory.Faker('pydecimal', left_digits=3, right_digits=2,
                                      positive=True, min_value=50, max_value=120)
    emergency_contact = factory.Sequence(lambda n: f"{9000000000 + n}")


class BookingFactory(DjangoModelFactory):
    class Meta:
        model = Booking

    user           = factory.SubFactory(GymUserFactory)
    user_name      = factory.LazyAttribute(lambda _: fake.name())
    user_phone     = factory.Sequence(lambda n: f"{1000000000 + n}")
    trainer        = factory.SubFactory(TrainerFactory)
    program        = factory.SubFactory(ProgramFactory)
    preferred_date = factory.Faker('future_date', end_date='+30d')
    preferred_time = factory.Iterator(['morning', 'afternoon', 'evening'])
    message        = factory.LazyAttribute(lambda _: fake.sentence())