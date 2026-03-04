import json

import pytest
from django.test import Client

from apps.accounts.tests.factories import UserFactory
from apps.analytics.models import Click
from apps.links.tests.factories import LinkFactory


@pytest.mark.django_db
class TestRecentClicksAPI:
    def test_unauthenticated_returns_403(self, client):
        """Anonymous users get a 403 from the recent-clicks API."""
        response = client.get('/analytics/api/recent-clicks/')
        assert response.status_code == 403

    def test_returns_only_own_links(self, client):
        """API only returns clicks belonging to the authenticated user's links."""
        owner = UserFactory()
        other = UserFactory()
        own_link = LinkFactory(owner=owner, short_code='own01')
        other_link = LinkFactory(owner=other, short_code='oth01')
        Click.objects.create(link=own_link, ip_address='1.2.3.4')
        Click.objects.create(link=other_link, ip_address='5.6.7.8')

        client.force_login(owner)
        response = client.get('/analytics/api/recent-clicks/')
        data = json.loads(response.content)
        codes = [c['link'] for c in data['clicks']]
        assert 'own01' in codes
        assert 'oth01' not in codes

    def test_returns_last_20_clicks(self, client):
        """API caps results at 20 clicks."""
        user = UserFactory()
        link = LinkFactory(owner=user, short_code='many1')
        for _ in range(25):
            Click.objects.create(link=link, ip_address='1.2.3.4')

        client.force_login(user)
        response = client.get('/analytics/api/recent-clicks/')
        data = json.loads(response.content)
        assert len(data['clicks']) == 20

    def test_response_is_valid_json(self, client):
        """API returns well-formed JSON with a 'clicks' key."""
        user = UserFactory()
        client.force_login(user)
        response = client.get('/analytics/api/recent-clicks/')
        assert response['Content-Type'] == 'application/json'
        data = json.loads(response.content)
        assert 'clicks' in data


@pytest.mark.django_db
class TestLinkDetailAnalytics:
    def test_shows_total_click_count(self, client):
        """Link detail page displays the total click count."""
        user = UserFactory()
        link = LinkFactory(owner=user, short_code='det01', click_count=42)
        client.force_login(user)
        response = client.get(f'/links/{link.pk}/')
        assert response.status_code == 200
        assert '42' in response.content.decode()

    def test_shows_top_countries(self, client):
        """Link detail page lists top countries by click count."""
        user = UserFactory()
        link = LinkFactory(owner=user, short_code='geo01')
        for _ in range(5):
            Click.objects.create(link=link, country='Germany', country_code='DE')
        for _ in range(3):
            Click.objects.create(link=link, country='France', country_code='FR')

        client.force_login(user)
        response = client.get(f'/links/{link.pk}/')
        content = response.content.decode()
        assert 'Germany' in content
        assert 'France' in content

    def test_cannot_view_other_users_link_stats(self, client):
        """Users cannot view analytics for links they don't own."""
        owner = UserFactory()
        other = UserFactory()
        link = LinkFactory(owner=owner, short_code='priv1')
        client.force_login(other)
        response = client.get(f'/links/{link.pk}/')
        assert response.status_code == 404
