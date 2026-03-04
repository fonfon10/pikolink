import pytest
from django.db import IntegrityError

from apps.links.models import Link
from apps.links.tests.factories import LinkFactory
from apps.links.utils import generate_short_code


@pytest.mark.django_db
class TestLink:
    def test_link_creation(self):
        """A Link can be created with required fields."""
        link = LinkFactory(original_url='https://example.com/long-path')
        assert link.pk is not None
        assert link.original_url == 'https://example.com/long-path'
        assert link.owner is not None

    def test_short_code_is_unique(self):
        """Two links cannot share the same short_code."""
        LinkFactory(short_code='abcde')
        with pytest.raises(IntegrityError):
            LinkFactory(short_code='abcde')

    def test_get_short_url_returns_pikolink_url(self):
        """get_short_url() returns the full pikolink.com URL."""
        link = LinkFactory(short_code='Xy12z')
        assert link.get_short_url() == 'https://pikolink.com/Xy12z'

    def test_click_count_defaults_zero(self):
        """New links start with click_count=0."""
        link = LinkFactory()
        assert link.click_count == 0


@pytest.mark.django_db
class TestGenerateShortCode:
    def test_generates_5_char_code(self):
        """Default code length is 5 characters."""
        code = generate_short_code()
        assert len(code) == 5

    def test_code_is_alphanumeric(self):
        """Code contains only letters and digits."""
        code = generate_short_code()
        assert code.isalnum()

    def test_codes_are_unique_on_repeated_calls(self):
        """Multiple calls return distinct codes."""
        codes = {generate_short_code() for _ in range(50)}
        assert len(codes) == 50
