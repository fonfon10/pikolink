import pytest
from django.db import IntegrityError

from apps.accounts.models import CustomUser
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestCustomUser:
    def test_create_user_with_email(self):
        """CustomUser can be created with email as username."""
        user = UserFactory(email='alice@example.com')
        assert user.pk is not None
        assert user.email == 'alice@example.com'
        assert user.check_password('testpass123')

    def test_email_must_be_unique(self):
        """Creating two users with same email raises IntegrityError."""
        UserFactory(email='dupe@example.com', username='user1')
        with pytest.raises(IntegrityError):
            UserFactory(email='dupe@example.com', username='user2')

    def test_email_verified_defaults_false(self):
        """New user has email_verified=False."""
        user = CustomUser.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='testpass123',
        )
        assert user.email_verified is False

    def test_is_super_admin_defaults_false(self):
        """New user has is_super_admin=False."""
        user = CustomUser.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='testpass123',
        )
        assert user.is_super_admin is False

    def test_str_returns_email(self):
        """__str__ returns the user's email."""
        user = UserFactory(email='str@example.com')
        assert str(user) == 'str@example.com'

    def test_username_field_is_email(self):
        """USERNAME_FIELD is set to email."""
        assert CustomUser.USERNAME_FIELD == 'email'

    def test_required_fields_includes_username(self):
        """REQUIRED_FIELDS includes username."""
        assert 'username' in CustomUser.REQUIRED_FIELDS
