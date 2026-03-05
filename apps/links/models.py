from django.conf import settings
from django.db import models


class Link(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='links'
    )
    team = models.ForeignKey(
        'teams.Team', null=True, blank=True, on_delete=models.SET_NULL
    )
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    title = models.CharField(max_length=255, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    customers = models.ManyToManyField(
        'customers.Customer', blank=True, related_name='links'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_short_url(self):
        return f'https://pikolink.com/{self.short_code}'

    def __str__(self):
        return f'{self.short_code} -> {self.original_url[:60]}'
