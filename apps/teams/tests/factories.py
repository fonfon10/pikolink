import factory
from django.utils.text import slugify
from faker import Faker

from apps.accounts.tests.factories import UserFactory
from apps.teams.models import Team, TeamMembership

fake = Faker()


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.LazyAttribute(lambda _: fake.unique.company())
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    owner = factory.SubFactory(UserFactory)


class TeamMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TeamMembership

    team = factory.SubFactory(TeamFactory)
    user = factory.SubFactory(UserFactory)
    role = 'viewer'
