import secrets
import string

ALPHABET = string.ascii_letters + string.digits  # 62 chars


def generate_short_code(length=5):
    from .models import Link

    for _ in range(10):
        code = ''.join(secrets.choice(ALPHABET) for _ in range(length))
        if not Link.objects.filter(short_code=code).exists():
            return code
    raise RuntimeError('Could not generate unique short code')
