import pytest
from django.db import IntegrityError

from apps.accounts.tests.factories import UserFactory
from apps.teams.models import Team, TeamMembership
from apps.teams.tests.factories import TeamFactory, TeamMembershipFactory


@pytest.mark.django_db
class TestTeam:
    def test_team_creation(self):
        """A Team can be created with name, slug, and owner."""
        team = TeamFactory(name='Acme Corp', slug='acme-corp')
        assert team.pk is not None
        assert team.name == 'Acme Corp'
        assert team.slug == 'acme-corp'
        assert team.owner is not None

    def test_team_slug_is_unique(self):
        """Two teams cannot share the same slug."""
        TeamFactory(slug='unique-slug')
        with pytest.raises(IntegrityError):
            TeamFactory(slug='unique-slug')


@pytest.mark.django_db
class TestTeamMembership:
    def test_membership_default_role_is_viewer(self):
        """New memberships default to the 'viewer' role."""
        membership = TeamMembershipFactory()
        assert membership.role == 'viewer'

    def test_user_cannot_join_same_team_twice(self):
        """A user cannot have two memberships in the same team."""
        team = TeamFactory()
        user = UserFactory()
        TeamMembership.objects.create(team=team, user=user, role='viewer')
        with pytest.raises(IntegrityError):
            TeamMembership.objects.create(team=team, user=user, role='editor')

    def test_owner_can_invite_members(self):
        """The team owner can add members to the team."""
        owner = UserFactory()
        team = TeamFactory(owner=owner)
        invitee = UserFactory()
        membership = TeamMembership.objects.create(
            team=team, user=invitee, role='editor'
        )
        assert membership.pk is not None
        assert membership.user == invitee
        assert membership.team == team
        assert membership.role == 'editor'
