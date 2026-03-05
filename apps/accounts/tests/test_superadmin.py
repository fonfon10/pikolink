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


@pytest.mark.django_db
class TestAdminToggleUser:
    def test_toggle_deactivates_active_user(self, client, super_admin):
        user = UserFactory(is_active=True)
        client.force_login(super_admin)
        response = client.post(f'/super-admin/users/{user.pk}/toggle/')
        user.refresh_from_db()
        assert not user.is_active
        assert response.status_code == 302

    def test_toggle_activates_inactive_user(self, client, super_admin):
        user = UserFactory(is_active=False)
        client.force_login(super_admin)
        client.post(f'/super-admin/users/{user.pk}/toggle/')
        user.refresh_from_db()
        assert user.is_active

    def test_non_admin_cannot_toggle(self, client, regular_user):
        user = UserFactory()
        client.force_login(regular_user)
        response = client.post(f'/super-admin/users/{user.pk}/toggle/')
        assert response.status_code == 403

    def test_get_not_allowed(self, client, super_admin):
        user = UserFactory()
        client.force_login(super_admin)
        response = client.get(f'/super-admin/users/{user.pk}/toggle/')
        assert response.status_code == 405


@pytest.mark.django_db
class TestAdminDeleteUser:
    def test_delete_removes_user(self, client, super_admin):
        user = UserFactory(email='todelete@example.com')
        client.force_login(super_admin)
        response = client.post(f'/super-admin/users/{user.pk}/delete/')
        from apps.accounts.models import CustomUser
        assert not CustomUser.objects.filter(email='todelete@example.com').exists()
        assert response.status_code == 302

    def test_cannot_delete_self(self, client, super_admin):
        client.force_login(super_admin)
        response = client.post(f'/super-admin/users/{super_admin.pk}/delete/')
        from apps.accounts.models import CustomUser
        assert CustomUser.objects.filter(pk=super_admin.pk).exists()

    def test_non_admin_cannot_delete(self, client, regular_user):
        user = UserFactory()
        client.force_login(regular_user)
        response = client.post(f'/super-admin/users/{user.pk}/delete/')
        assert response.status_code == 403


@pytest.mark.django_db
class TestAdminResetPassword:
    def test_reset_sends_email(self, client, super_admin, mailoutbox):
        user = UserFactory(email='reset@example.com')
        from allauth.account.models import EmailAddress
        EmailAddress.objects.create(user=user, email=user.email, verified=True, primary=True)
        client.force_login(super_admin)
        response = client.post(f'/super-admin/users/{user.pk}/reset-password/')
        assert response.status_code == 302
        assert len(mailoutbox) == 1

    def test_non_admin_cannot_reset(self, client, regular_user):
        user = UserFactory()
        client.force_login(regular_user)
        response = client.post(f'/super-admin/users/{user.pk}/reset-password/')
        assert response.status_code == 403


@pytest.mark.django_db
class TestAdminChangeRole:
    def test_change_to_super_admin(self, client, super_admin):
        user = UserFactory()
        client.force_login(super_admin)
        client.post(f'/super-admin/users/{user.pk}/change-role/', {'role': 'super_admin'})
        user.refresh_from_db()
        assert user.is_super_admin
        assert user.is_staff

    def test_change_to_staff(self, client, super_admin):
        user = UserFactory(is_super_admin=True, is_staff=True)
        client.force_login(super_admin)
        client.post(f'/super-admin/users/{user.pk}/change-role/', {'role': 'staff'})
        user.refresh_from_db()
        assert not user.is_super_admin
        assert user.is_staff

    def test_change_to_user(self, client, super_admin):
        user = UserFactory(is_staff=True)
        client.force_login(super_admin)
        client.post(f'/super-admin/users/{user.pk}/change-role/', {'role': 'user'})
        user.refresh_from_db()
        assert not user.is_super_admin
        assert not user.is_staff

    def test_cannot_change_own_role(self, client, super_admin):
        client.force_login(super_admin)
        client.post(f'/super-admin/users/{super_admin.pk}/change-role/', {'role': 'user'})
        super_admin.refresh_from_db()
        assert super_admin.is_super_admin

    def test_non_admin_cannot_change_role(self, client, regular_user):
        user = UserFactory()
        client.force_login(regular_user)
        response = client.post(f'/super-admin/users/{user.pk}/change-role/', {'role': 'super_admin'})
        assert response.status_code == 403
