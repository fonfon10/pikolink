import factory
from faker import Faker

from apps.accounts.tests.factories import UserFactory
from apps.customers.models import Customer

fake = Faker()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    owner = factory.SubFactory(UserFactory)
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    company = factory.LazyAttribute(lambda _: fake.company())
