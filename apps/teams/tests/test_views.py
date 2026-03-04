import pytest

from apps.accounts.tests.factories import UserFactory
from apps.teams.models import Team, TeamMembership
from apps.teams.tests.factories import TeamFactory


@pytest.mark.django_db
class TestCreateTeamView:
    def test_create_team_page_loads(self, client):
        """Create team page returns 200 for authenticated users."""
        user = UserFactory()
        client.force_login(user)
        response = client.get('/teams/create/')
        assert response.status_code == 200

    def test_create_team_requires_login(self, client):
        """Anonymous users are redirected to login."""
        response = client.get('/teams/create/')
        assert response.status_code == 302

    def test_create_team_saves_team(self, client):
        """Submitting the form creates a Team owned by the user."""
        user = UserFactory()
        client.force_login(user)
        response = client.post('/teams/create/', {'name': 'My Team'})
        assert Team.objects.filter(owner=user, name='My Team').exists()
        team = Team.objects.get(owner=user)
        assert team.slug == 'my-team'

    def test_create_team_redirects_to_team_dashboard(self, client):
        """After creating a team the user is redirected to its dashboard."""
        user = UserFactory()
        client.force_login(user)
        response = client.post('/teams/create/', {'name': 'New Team'})
        team = Team.objects.get(owner=user)
        assert response.status_code == 302
        assert f'/teams/{team.slug}/' in response['Location']


@pytest.mark.django_db
class TestTeamDashboardView:
    def test_team_dashboard_loads_for_owner(self, client):
        """Team owner can view the team dashboard."""
        user = UserFactory()
        team = TeamFactory(owner=user, slug='my-team')
        client.force_login(user)
        response = client.get(f'/teams/{team.slug}/')
        assert response.status_code == 200
        assert team.name in response.content.decode()

    def test_team_dashboard_loads_for_member(self, client):
        """A team member can view the team dashboard."""
        team = TeamFactory(slug='member-team')
        member = UserFactory()
        TeamMembership.objects.create(team=team, user=member, role='viewer')
        client.force_login(member)
        response = client.get(f'/teams/{team.slug}/')
        assert response.status_code == 200

    def test_team_dashboard_denied_for_non_member(self, client):
        """Non-members get 404 for a team dashboard."""
        team = TeamFactory(slug='secret')
        outsider = UserFactory()
        client.force_login(outsider)
        response = client.get(f'/teams/{team.slug}/')
        assert response.status_code == 404


@pytest.mark.django_db
class TestInviteMemberView:
    def test_owner_can_invite_member(self, client):
        """Team owner can invite a user by email."""
        owner = UserFactory()
        invitee = UserFactory(email='invitee@example.com')
        team = TeamFactory(owner=owner, slug='inv-team')
        client.force_login(owner)
        response = client.post(f'/teams/{team.slug}/invite/', {
            'email': 'invitee@example.com',
            'role': 'editor',
        })
        assert response.status_code == 302
        assert TeamMembership.objects.filter(team=team, user=invitee, role='editor').exists()

    def test_non_owner_cannot_invite(self, client):
        """Non-owners cannot invite members."""
        owner = UserFactory()
        member = UserFactory()
        team = TeamFactory(owner=owner, slug='no-inv')
        TeamMembership.objects.create(team=team, user=member, role='viewer')
        client.force_login(member)
        response = client.post(f'/teams/{team.slug}/invite/', {
            'email': 'someone@example.com',
            'role': 'viewer',
        })
        assert response.status_code == 403
