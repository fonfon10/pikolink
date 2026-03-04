import pytest

from apps.accounts.tests.factories import UserFactory
from apps.links.tests.factories import LinkFactory
from apps.teams.tests.factories import TeamFactory


@pytest.fixture
def super_admin():
    return UserFactory(is_super_admin=True, is_staff=True)


@pytest.fixture
def regular_user():
    return UserFactory()


@pytest.mark.django_db
class TestSuperAdminAccess:
    def test_non_admin_gets_403_on_dashboard(self, client, regular_user):
        """Regular users are denied access to super admin dashboard."""
        client.force_login(regular_user)
        response = client.get('/super-admin/')
        assert response.status_code == 403

    def test_anonymous_gets_403_on_dashboard(self, client):
        """Anonymous users are denied access to super admin dashboard."""
        response = client.get('/super-admin/')
        assert response.status_code == 403

    def test_super_admin_can_access_dashboard(self, client, super_admin):
        """Super admins can access the dashboard."""
        client.force_login(super_admin)
        response = client.get('/super-admin/')
        assert response.status_code == 200

    def test_super_admin_can_access_users(self, client, super_admin):
        """Super admins can access the users page."""
        client.force_login(super_admin)
        response = client.get('/super-admin/users/')
        assert response.status_code == 200

    def test_super_admin_can_access_links(self, client, super_admin):
        """Super admins can access the links page."""
        client.force_login(super_admin)
        response = client.get('/super-admin/links/')
        assert response.status_code == 200

    def test_super_admin_can_access_teams(self, client, super_admin):
        """Super admins can access the teams page."""
        client.force_login(super_admin)
        response = client.get('/super-admin/teams/')
        assert response.status_code == 200


@pytest.mark.django_db
class TestSuperAdminDashboard:
    def test_dashboard_shows_total_users(self, client, super_admin):
        """Dashboard displays total user count."""
        UserFactory()
        UserFactory()
        client.force_login(super_admin)
        response = client.get('/super-admin/')
        content = response.content.decode()
        # super_admin + 2 users = 3
        assert '3' in content

    def test_dashboard_shows_total_links(self, client, super_admin):
        """Dashboard displays total link count."""
        LinkFactory()
        LinkFactory()
        client.force_login(super_admin)
        response = client.get('/super-admin/')
        assert '2' in response.content.decode()


@pytest.mark.django_db
class TestSuperAdminUsers:
    def test_users_page_lists_all_users(self, client, super_admin):
        """Users page shows all registered users."""
        user = UserFactory(email='listed@example.com')
        client.force_login(super_admin)
        response = client.get('/super-admin/users/')
        assert 'listed@example.com' in response.content.decode()


@pytest.mark.django_db
class TestSuperAdminLinks:
    def test_links_page_lists_all_links(self, client, super_admin):
        """Links page shows all links across users."""
        link = LinkFactory(short_code='adm01')
        client.force_login(super_admin)
        response = client.get('/super-admin/links/')
        assert 'adm01' in response.content.decode()


@pytest.mark.django_db
class TestSuperAdminTeams:
    def test_teams_page_lists_all_teams(self, client, super_admin):
        """Teams page shows all teams."""
        team = TeamFactory(name='Admin Team', slug='admin-team')
        client.force_login(super_admin)
        response = client.get('/super-admin/teams/')
        assert 'Admin Team' in response.content.decode()
