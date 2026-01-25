from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from links.models import Click, Customer, Link


User = get_user_model()


class PikoLinkCoreTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="pass12345"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="pass12345"
        )

        self.customer1 = Customer.objects.create(
            first_name="Serge",
            last_name="Lafontaine",
            email="serge.lafontaine@ttiinc.com",
            company_name="TTI",
            comments="",
        )

    def test_app_pages_require_login(self):
        # not logged in
        resp = self.client.get("/app/links/new")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp["Location"])

        resp = self.client.get("/app/links")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp["Location"])

        resp = self.client.get("/app/clicks")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp["Location"])

    def test_create_customer_flow(self):
        self.client.login(username="user1", password="pass12345")

        resp = self.client.get("/app/customers/new")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            "/app/customers/new",
            data={
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@example.com",
                "company_name": "Acme",
                "comments": "note",
            },
        )
        # redirect back somewhere (create_customer redirects)
        self.assertEqual(resp.status_code, 302)

        self.assertTrue(Customer.objects.filter(email="john.smith@example.com").exists())

    def test_create_link_and_list_scoped_to_user(self):
        self.client.login(username="user1", password="pass12345")

        resp = self.client.post(
            "/app/links/new",
            data={
                "destination_url": "https://example.com",
                "campaign_name": "Camp1",
                "notes": "n",
                "customer": self.customer1.id,
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Link.objects.filter(created_by=self.user1).exists())

        # user1 sees it
        resp = self.client.get("/app/links")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "example.com")

        # user2 should not see user1 links
        self.client.logout()
        self.client.login(username="user2", password="pass12345")
        resp = self.client.get("/app/links")
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "example.com")

    def test_public_redirect_creates_click_and_redirects(self):
        link = Link.objects.create(
            created_by=self.user1,
            destination_url="https://example.com/abc",
            campaign_name="",
            notes="",
            customer=self.customer1,
        )

        resp = self.client.get(f"/{link.code}/")
        self.assertEqual(resp.status_code, 301)
        self.assertEqual(resp["Location"], "https://example.com/abc")

        self.assertEqual(Click.objects.filter(link=link).count(), 1)
        click = Click.objects.get(link=link)
        self.assertEqual(click.customer, self.customer1)

    def test_clicks_list_scoped_to_user(self):
        link1 = Link.objects.create(
            created_by=self.user1,
            destination_url="https://example.com/1",
            campaign_name="",
            notes="",
            customer=self.customer1,
        )
        link2 = Link.objects.create(
            created_by=self.user2,
            destination_url="https://example.com/2",
            campaign_name="",
            notes="",
            customer=self.customer1,
        )
        Click.objects.create(link=link1, customer=self.customer1)
        Click.objects.create(link=link2, customer=self.customer1)

        self.client.login(username="user1", password="pass12345")
        resp = self.client.get("/app/clicks")
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, link1.code)
        self.assertNotContains(resp, link2.code)

    def test_customer_display_label_format(self):
        self.assertEqual(self.customer1.display_label(), "SLafontaine/TTI")