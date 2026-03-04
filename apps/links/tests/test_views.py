import pytest

from apps.accounts.tests.factories import UserFactory
from apps.links.models import Link
from apps.links.tests.factories import LinkFactory


@pytest.mark.django_db
class TestDashboardView:
    def test_dashboard_shows_users_links(self, client):
        """Dashboard lists the authenticated user's links."""
        user = UserFactory()
        link = LinkFactory(owner=user, short_code='dash1', original_url='https://example.com')
        client.force_login(user)
        response = client.get('/dashboard/')
        content = response.content.decode()
        assert 'dash1' in content
        assert 'https://example.com' in content

    def test_dashboard_does_not_show_other_users_links(self, client):
        """Dashboard excludes links owned by other users."""
        user = UserFactory()
        other = UserFactory()
        LinkFactory(owner=other, short_code='other1')
        client.force_login(user)
        response = client.get('/dashboard/')
        assert 'other1' not in response.content.decode()

    def test_dashboard_shows_click_counts(self, client):
        """Dashboard displays each link's click count."""
        user = UserFactory()
        LinkFactory(owner=user, short_code='cnt99', click_count=99)
        client.force_login(user)
        response = client.get('/dashboard/')
        assert '99' in response.content.decode()

    def test_dashboard_has_create_link_button(self, client):
        """Dashboard contains a link/button to create a new link."""
        user = UserFactory()
        client.force_login(user)
        response = client.get('/dashboard/')
        assert 'create' in response.content.decode().lower()


@pytest.mark.django_db
class TestCreateLinkView:
    def test_create_link_page_loads(self, client):
        """The create-link page returns 200 for authenticated users."""
        user = UserFactory()
        client.force_login(user)
        response = client.get('/links/create/')
        assert response.status_code == 200

    def test_create_link_requires_login(self, client):
        """Anonymous users are redirected to login."""
        response = client.get('/links/create/')
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_create_link_saves_link(self, client):
        """Submitting the form creates a Link with auto-generated short_code."""
        user = UserFactory()
        client.force_login(user)
        response = client.post('/links/create/', {
            'original_url': 'https://example.com/my-page',
            'title': 'My Page',
        })
        assert Link.objects.filter(owner=user, original_url='https://example.com/my-page').exists()
        link = Link.objects.get(owner=user)
        assert len(link.short_code) == 5
        assert link.title == 'My Page'

    def test_create_link_redirects_to_dashboard(self, client):
        """After creating a link the user is redirected to the dashboard."""
        user = UserFactory()
        client.force_login(user)
        response = client.post('/links/create/', {
            'original_url': 'https://example.com/redirect-test',
        })
        assert response.status_code == 302
        assert '/dashboard/' in response['Location']


@pytest.mark.django_db
class TestRealtimeView:
    def test_realtime_page_loads(self, client):
        """The real-time analytics page returns 200 for authenticated users."""
        user = UserFactory()
        client.force_login(user)
        response = client.get('/analytics/realtime/')
        assert response.status_code == 200

    def test_realtime_requires_login(self, client):
        """Anonymous users are redirected to login."""
        response = client.get('/analytics/realtime/')
        assert response.status_code == 302
