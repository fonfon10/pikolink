import json

import pytest
from django.test import Client

from apps.accounts.tests.factories import UserFactory
from apps.customers.models import Customer
from apps.links.tests.factories import LinkFactory

from .factories import CustomerFactory


@pytest.mark.django_db
class TestCustomerList:
    def test_requires_login(self, client):
        response = client.get('/customers/')
        assert response.status_code == 302

    def test_list_page_loads(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.get('/customers/')
        assert response.status_code == 200

    def test_shows_own_customers(self, client):
        user = UserFactory()
        CustomerFactory(owner=user, first_name='Alice', last_name='Smith')
        CustomerFactory()  # another user's customer
        client.force_login(user)
        response = client.get('/customers/')
        content = response.content.decode()
        assert 'Alice' in content
        assert Customer.objects.exclude(owner=user).first().first_name not in content

    def test_search_filters(self, client):
        user = UserFactory()
        CustomerFactory(owner=user, first_name='Alice', last_name='Smith')
        CustomerFactory(owner=user, first_name='Bob', last_name='Jones')
        client.force_login(user)
        response = client.get('/customers/?q=alice')
        content = response.content.decode()
        assert 'Alice' in content
        assert 'Bob' not in content


@pytest.mark.django_db
class TestCustomerAdd:
    def test_requires_login(self, client):
        response = client.get('/customers/add/')
        assert response.status_code == 302

    def test_add_page_loads(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.get('/customers/add/')
        assert response.status_code == 200

    def test_add_customer(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.post('/customers/add/', {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@example.com',
            'company': 'Acme',
        })
        assert response.status_code == 302
        assert Customer.objects.filter(owner=user, first_name='Jane').exists()

    def test_add_requires_name(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.post('/customers/add/', {
            'first_name': '',
            'last_name': '',
        })
        assert response.status_code == 200
        assert Customer.objects.count() == 0


@pytest.mark.django_db
class TestCustomerEdit:
    def test_edit_page_loads(self, client):
        customer = CustomerFactory()
        client.force_login(customer.owner)
        response = client.get(f'/customers/{customer.pk}/edit/')
        assert response.status_code == 200

    def test_edit_saves_changes(self, client):
        customer = CustomerFactory()
        client.force_login(customer.owner)
        response = client.post(f'/customers/{customer.pk}/edit/', {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': '',
            'company': '',
        })
        assert response.status_code == 302
        customer.refresh_from_db()
        assert customer.first_name == 'Updated'

    def test_cannot_edit_others_customer(self, client):
        customer = CustomerFactory()
        other_user = UserFactory()
        client.force_login(other_user)
        response = client.get(f'/customers/{customer.pk}/edit/')
        assert response.status_code == 404


@pytest.mark.django_db
class TestCustomerDelete:
    def test_delete_requires_post(self, client):
        customer = CustomerFactory()
        client.force_login(customer.owner)
        response = client.get(f'/customers/{customer.pk}/delete/')
        assert response.status_code == 405

    def test_delete_customer(self, client):
        customer = CustomerFactory()
        client.force_login(customer.owner)
        response = client.post(f'/customers/{customer.pk}/delete/')
        assert response.status_code == 302
        assert not Customer.objects.filter(pk=customer.pk).exists()

    def test_cannot_delete_others_customer(self, client):
        customer = CustomerFactory()
        other_user = UserFactory()
        client.force_login(other_user)
        response = client.post(f'/customers/{customer.pk}/delete/')
        assert response.status_code == 404


@pytest.mark.django_db
class TestCustomerImport:
    def test_import_page_loads(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.get('/customers/import/')
        assert response.status_code == 200

    def test_import_csv(self, client):
        from io import BytesIO
        user = UserFactory()
        client.force_login(user)
        csv_content = b'first_name,last_name,email,company\nAlice,Smith,alice@test.com,Acme\nBob,Jones,,\n'
        f = BytesIO(csv_content)
        f.name = 'customers.csv'
        response = client.post('/customers/import/', {'csv_file': f})
        assert response.status_code == 302
        assert Customer.objects.filter(owner=user).count() == 2

    def test_import_skips_invalid_rows(self, client):
        from io import BytesIO
        user = UserFactory()
        client.force_login(user)
        csv_content = b'first_name,last_name,email,company\n,Smith,,\nBob,,,\nAlice,Jones,,\n'
        f = BytesIO(csv_content)
        f.name = 'customers.csv'
        response = client.post('/customers/import/', {'csv_file': f})
        assert response.status_code == 302
        # Only Alice Jones is valid (first_name + last_name both present)
        assert Customer.objects.filter(owner=user).count() == 1


@pytest.mark.django_db
class TestCustomerSearchAPI:
    def test_requires_login(self, client):
        response = client.get('/customers/api/search/?q=test')
        assert response.status_code == 302

    def test_returns_json(self, client):
        user = UserFactory()
        CustomerFactory(owner=user, first_name='Alice', last_name='Smith')
        client.force_login(user)
        response = client.get('/customers/api/search/?q=alice')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) == 1
        assert data[0]['name'] == 'Alice Smith'

    def test_does_not_return_others_customers(self, client):
        user = UserFactory()
        CustomerFactory(first_name='Alice', last_name='Other')
        client.force_login(user)
        response = client.get('/customers/api/search/?q=alice')
        data = json.loads(response.content)
        assert len(data) == 0

    def test_empty_query(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.get('/customers/api/search/?q=')
        data = json.loads(response.content)
        assert data == []


@pytest.mark.django_db
class TestCustomerQuickCreate:
    def test_requires_login(self, client):
        response = client.post(
            '/customers/api/quick-create/',
            json.dumps({'first_name': 'A', 'last_name': 'B'}),
            content_type='application/json',
        )
        assert response.status_code == 302

    def test_creates_customer(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.post(
            '/customers/api/quick-create/',
            json.dumps({'first_name': 'Jane', 'last_name': 'Doe', 'email': 'j@test.com', 'company': 'Acme'}),
            content_type='application/json',
        )
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data['name'] == 'Jane Doe'
        assert Customer.objects.filter(pk=data['id'], owner=user).exists()

    def test_requires_first_and_last_name(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.post(
            '/customers/api/quick-create/',
            json.dumps({'first_name': '', 'last_name': 'Doe'}),
            content_type='application/json',
        )
        data = json.loads(response.content)
        assert response.status_code == 400
        assert 'error' in data

    def test_rejects_get(self, client):
        user = UserFactory()
        client.force_login(user)
        response = client.get('/customers/api/quick-create/')
        assert response.status_code == 405


@pytest.mark.django_db
class TestLinkCustomerTagging:
    def test_create_link_with_customers(self, client):
        user = UserFactory()
        c1 = CustomerFactory(owner=user)
        c2 = CustomerFactory(owner=user)
        client.force_login(user)
        response = client.post('/links/create/', {
            'original_url': 'https://example.com',
            'title': 'Test',
            'customer_ids': f'{c1.pk},{c2.pk}',
        })
        assert response.status_code == 302
        from apps.links.models import Link
        link = Link.objects.get(owner=user)
        assert set(link.customers.values_list('pk', flat=True)) == {c1.pk, c2.pk}

    def test_cannot_tag_others_customers(self, client):
        user = UserFactory()
        other_customer = CustomerFactory()  # belongs to another user
        client.force_login(user)
        response = client.post('/links/create/', {
            'original_url': 'https://example.com',
            'title': 'Test',
            'customer_ids': str(other_customer.pk),
        })
        assert response.status_code == 302
        from apps.links.models import Link
        link = Link.objects.get(owner=user)
        assert link.customers.count() == 0

    def test_link_detail_shows_customers(self, client):
        user = UserFactory()
        customer = CustomerFactory(owner=user, first_name='TaggedUser', last_name='Here')
        link = LinkFactory(owner=user)
        link.customers.add(customer)
        client.force_login(user)
        response = client.get(f'/links/{link.pk}/')
        assert 'TaggedUser' in response.content.decode()
