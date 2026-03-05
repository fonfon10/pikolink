import pytest

from apps.customers.models import Customer

from .factories import CustomerFactory


@pytest.mark.django_db
class TestCustomer:
    def test_create_customer(self):
        """Customer can be created with required fields."""
        customer = CustomerFactory()
        assert Customer.objects.filter(pk=customer.pk).exists()

    def test_str_returns_full_name(self):
        """String representation is first + last name."""
        customer = CustomerFactory(first_name='Jane', last_name='Doe')
        assert str(customer) == 'Jane Doe'

    def test_owner_privacy(self):
        """Customers belong to their owner only."""
        c1 = CustomerFactory()
        c2 = CustomerFactory()
        assert c1.owner != c2.owner or c1.pk != c2.pk
        own_customers = Customer.objects.filter(owner=c1.owner)
        assert c1 in own_customers
        assert c2 not in own_customers

    def test_optional_fields_blank(self):
        """Email and company can be blank."""
        customer = CustomerFactory(email='', company='')
        customer.full_clean()
        assert customer.email == ''
        assert customer.company == ''

    def test_ordering(self):
        """Customers are ordered by last_name, first_name."""
        from apps.accounts.tests.factories import UserFactory
        owner = UserFactory()
        CustomerFactory(owner=owner, last_name='Zulu', first_name='Alpha')
        CustomerFactory(owner=owner, last_name='Alpha', first_name='Beta')
        names = list(
            Customer.objects.filter(owner=owner).values_list('last_name', flat=True)
        )
        assert names == ['Alpha', 'Zulu']
