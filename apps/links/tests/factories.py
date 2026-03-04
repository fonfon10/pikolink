import factory
from faker import Faker

from apps.accounts.tests.factories import UserFactory
from apps.links.models import Link
from apps.links.utils import generate_short_code

fake = Faker()


class LinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Link

    owner = factory.SubFactory(UserFactory)
    original_url = factory.LazyAttribute(lambda _: fake.url())
    short_code = factory.LazyAttribute(lambda _: generate_short_code())
    is_active = True
