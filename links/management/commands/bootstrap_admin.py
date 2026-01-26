# links/management/commands/bootstrap_admin.py
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or reset admin user from ADMIN_EMAIL and ADMIN_PASSWORD"

    def handle(self, *args, **options):
        email = (os.getenv("ADMIN_EMAIL") or "").strip().lower()
        password = os.getenv("ADMIN_PASSWORD") or ""

        if not email or not password:
            self.stdout.write(self.style.WARNING("ADMIN_EMAIL or ADMIN_PASSWORD not set"))
            return

        User = get_user_model()

        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            # Create user safely for custom User models
            if hasattr(User, "username"):
                user = User(username=email, email=email)
            else:
                user = User(email=email)

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Admin ensured: {email}"))