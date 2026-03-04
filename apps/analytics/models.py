from django.db import models


class Click(models.Model):
    link = models.ForeignKey(
        'links.Link', on_delete=models.CASCADE, related_name='clicks'
    )
    clicked_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=2, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)

    class Meta:
        ordering = ['-clicked_at']
        indexes = [
            models.Index(fields=['link', 'clicked_at']),
            models.Index(fields=['country_code']),
        ]

    def __str__(self):
        return f'Click on {self.link.short_code} at {self.clicked_at}'
