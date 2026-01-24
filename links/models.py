from __future__ import annotations

import secrets
import string

from django.conf import settings
from django.db import models


def generate_code(length: int = 6) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class Customer(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    company_name = models.CharField(max_length=120)
    comments = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def display_label(self) -> str:
        first_initial = self.first_name[:1] if self.first_name else ""
        last = self.last_name or ""
        company = self.company_name or ""
        return f"{first_initial}{last}/{company}"

    def __str__(self) -> str:
        return self.display_label()


class Link(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="links"
    )

    code = models.CharField(max_length=12, unique=True, default=generate_code)
    destination_url = models.URLField()

    campaign_name = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="links")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.code} -> {self.destination_url}"


class Click(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name="clicks")
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name="clicks"
    )

    clicked_at = models.DateTimeField(auto_now_add=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    # basic geo fields we can fill later
    country = models.CharField(max_length=2, blank=True)
    region = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)

    def __str__(self) -> str:
        who = self.customer.display_label() if self.customer else "Unknown"
        return f"{who} clicked {self.link.code} at {self.clicked_at}"