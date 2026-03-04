import pytest

from apps.analytics.models import Click
from apps.links.tests.factories import LinkFactory


@pytest.mark.django_db
class TestRedirectView:
    def test_valid_short_code_redirects_301(self, client):
        """A valid short code returns a 301 permanent redirect."""
        link = LinkFactory(short_code='abc12')
        response = client.get('/abc12/')
        assert response.status_code == 301

    def test_redirect_goes_to_original_url(self, client):
        """The redirect Location header points to original_url."""
        link = LinkFactory(short_code='redir', original_url='https://example.com/target')
        response = client.get('/redir/')
        assert response['Location'] == 'https://example.com/target'

    def test_invalid_short_code_returns_404(self, client):
        """A nonexistent short code returns 404."""
        response = client.get('/zzzzz/')
        assert response.status_code == 404

    def test_inactive_link_returns_410(self, client):
        """An inactive link returns 410 Gone."""
        LinkFactory(short_code='gone1', is_active=False)
        response = client.get('/gone1/')
        assert response.status_code == 410

    def test_redirect_increments_click_count(self, client):
        """Each redirect bumps click_count by 1."""
        link = LinkFactory(short_code='cnt01')
        client.get('/cnt01/')
        link.refresh_from_db()
        assert link.click_count == 1

    def test_redirect_creates_click_record(self, client):
        """A redirect creates a Click object tied to the link."""
        link = LinkFactory(short_code='clk01')
        client.get('/clk01/')
        assert Click.objects.filter(link=link).count() == 1

    def test_click_records_ip_address(self, client):
        """The Click record captures the client IP address."""
        link = LinkFactory(short_code='ip001')
        client.get('/ip001/')
        click = Click.objects.get(link=link)
        assert click.ip_address is not None
