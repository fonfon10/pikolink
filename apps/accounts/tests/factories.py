import factory
from faker import Faker

from apps.accounts.models import CustomUser

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    email = factory.LazyAttribute(lambda _: fake.unique.email())
    username = factory.LazyAttribute(lambda o: o.email.split('@')[0])
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    email_verified = True
