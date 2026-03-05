import pytest

from apps.accounts.models import CustomUser
from apps.accounts.tests.factories import UserFactory


@pytest.mark.django_db
class TestSignupView:
    def test_signup_page_loads(self, client):
        """GET /accounts/signup/ returns 200."""
        response = client.get('/accounts/signup/')
        assert response.status_code == 200

    def test_signup_page_contains_form(self, client):
        """Signup page contains a form with email and password fields."""
        response = client.get('/accounts/signup/')
        content = response.content.decode()
        assert 'email' in content.lower()
        assert 'password' in content.lower()

    def test_signup_creates_user(self, client):
        """POST to signup creates a new CustomUser."""
        client.post('/accounts/signup/', {
            'email': 'newuser@example.com',
            'password1': 'Str0ngP@ssw0rd!',
            'password2': 'Str0ngP@ssw0rd!',
        })
        assert CustomUser.objects.filter(email='newuser@example.com').exists()

    def test_signup_sends_verification_email(self, client, mailoutbox):
        """Signup sends a verification email."""
        client.post('/accounts/signup/', {
            'email': 'verify@example.com',
            'password1': 'Str0ngP@ssw0rd!',
            'password2': 'Str0ngP@ssw0rd!',
        })
        assert len(mailoutbox) == 1
        assert 'verify@example.com' in mailoutbox[0].to

    def test_signup_with_duplicate_email_fails(self, client):
        """Signup with an already-registered email does not create a second user."""
        UserFactory(email='taken@example.com')
        client.post('/accounts/signup/', {
            'email': 'taken@example.com',
            'password1': 'Str0ngP@ssw0rd!',
            'password2': 'Str0ngP@ssw0rd!',
        })
        assert CustomUser.objects.filter(email='taken@example.com').count() == 1

    def test_signup_redirects_after_success(self, client):
        """Successful signup redirects (302) to email verification page."""
        response = client.post('/accounts/signup/', {
            'email': 'redir@example.com',
            'password1': 'Str0ngP@ssw0rd!',
            'password2': 'Str0ngP@ssw0rd!',
        })
        assert response.status_code == 302


@pytest.mark.django_db
class TestLoginView:
    def test_login_page_loads(self, client):
        """GET /accounts/login/ returns 200."""
        response = client.get('/accounts/login/')
        assert response.status_code == 200

    def test_login_with_valid_credentials(self, client):
        """Login with correct email+password succeeds (302 redirect)."""
        user = UserFactory(email='login@example.com')
        from allauth.account.models import EmailAddress
        EmailAddress.objects.create(
            user=user, email=user.email, verified=True, primary=True
        )
        response = client.post('/accounts/login/', {
            'login': 'login@example.com',
            'password': 'testpass123',
        })
        assert response.status_code == 302

    def test_login_with_invalid_password_fails(self, client):
        """Login with wrong password stays on login page (200)."""
        user = UserFactory(email='badpass@example.com')
        from allauth.account.models import EmailAddress
        EmailAddress.objects.create(
            user=user, email=user.email, verified=True, primary=True
        )
        response = client.post('/accounts/login/', {
            'login': 'badpass@example.com',
            'password': 'wrongpassword',
        })
        assert response.status_code == 200

    def test_login_redirects_to_dashboard(self, client):
        """Successful login redirects to /dashboard/."""
        user = UserFactory(email='dash@example.com')
        from allauth.account.models import EmailAddress
        EmailAddress.objects.create(
            user=user, email=user.email, verified=True, primary=True
        )
        response = client.post('/accounts/login/', {
            'login': 'dash@example.com',
            'password': 'testpass123',
        })
        assert response.status_code == 302
        assert '/dashboard/' in response.url


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_redirects(self, client):
        """POST to logout redirects."""
        user = UserFactory(email='logout@example.com')
        client.force_login(user)
        response = client.post('/accounts/logout/')
        assert response.status_code == 302

    def test_logout_clears_session(self, client):
        """After logout, user is no longer authenticated."""
        user = UserFactory(email='session@example.com')
        client.force_login(user)
        client.post('/accounts/logout/')
        response = client.get('/dashboard/')
        # Should redirect to login since user is logged out
        assert response.status_code == 302
        assert '/accounts/login/' in response.url


@pytest.mark.django_db
class TestDashboardAccess:
    def test_authenticated_user_can_access_dashboard(self, client):
        """Logged-in user gets 200 on /dashboard/."""
        user = UserFactory(email='authed@example.com')
        client.force_login(user)
        response = client.get('/dashboard/')
        assert response.status_code == 200

    def test_anonymous_user_redirected_to_login(self, client):
        """Anonymous user is redirected to login from /dashboard/."""
        response = client.get('/dashboard/')
        assert response.status_code == 302
        assert '/accounts/login/' in response.url


@pytest.mark.django_db
class TestProfileView:
    def test_profile_page_loads(self, client):
        user = UserFactory(email='profile@example.com')
        client.force_login(user)
        response = client.get('/accounts/profile/')
        assert response.status_code == 200
        assert 'profile@example.com' in response.content.decode()

    def test_profile_update_name(self, client):
        user = UserFactory(email='namechange@example.com')
        client.force_login(user)
        response = client.post('/accounts/profile/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'namechange@example.com',
        })
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'

    def test_profile_update_email(self, client):
        user = UserFactory(email='oldemail@example.com')
        client.force_login(user)
        client.post('/accounts/profile/', {
            'first_name': '',
            'last_name': '',
            'email': 'newemail@example.com',
        })
        user.refresh_from_db()
        assert user.email == 'newemail@example.com'

    def test_profile_requires_login(self, client):
        response = client.get('/accounts/profile/')
        assert response.status_code == 302
        assert '/accounts/login/' in response.url
