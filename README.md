# PikoLink

PikoLink is a self-hosted URL shortener and analytics platform built with Django. It provides short link creation, click tracking with geographic data (country/city via GeoIP), real-time analytics, team collaboration, and a super admin panel.

## Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/pikolink.git
   cd pikolink
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements/development.txt
   ```

4. **Create a `.env` file** (optional — sane defaults are used for development):
   ```bash
   cp .env.example .env  # or create manually
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

   The app runs at `http://localhost:8000`. SQLite is used by default when no `DATABASE_URL` is set.

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | Production | `django-insecure-dev-key-change-me` | Django secret key |
| `DEBUG` | No | `False` | Enable debug mode |
| `DATABASE_URL` | Production | SQLite (dev) | PostgreSQL connection string |
| `ALLOWED_HOSTS` | Production | `localhost,127.0.0.1` | Comma-separated allowed hosts |
| `DJANGO_SETTINGS_MODULE` | No | `config.settings.development` | Settings module path |
| `EMAIL_HOST_USER` | Production | `''` | SMTP username (e.g., `pikolink@yahoo.com`) |
| `EMAIL_HOST_PASSWORD` | Production | `''` | SMTP password (Yahoo App Password) |
| `GEOIP_PATH` | No | `<project>/geoip/` | Path to GeoIP database directory |

## Running Tests

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run all tests
pytest

# Run tests without coverage enforcement
pytest --no-cov

# Run tests for a specific app
pytest apps/links/

# Run with verbose output
pytest -v
```

Tests use `pytest-django` with `factory-boy` fixtures. The coverage gate is set to 80% in `pytest.ini`.

## GeoIP Database Setup

PikoLink uses MaxMind's GeoLite2 database for geographic click tracking.

1. **Create a free MaxMind account** at [maxmind.com](https://www.maxmind.com/en/geolite2/signup).

2. **Download the GeoLite2-City database** (`.mmdb` format) from your MaxMind account dashboard.

3. **Place the database file** in the `geoip/` directory at the project root:
   ```
   pikolink/
     geoip/
       GeoLite2-City.mmdb
   ```

4. The `GEOIP_PATH` setting defaults to this location. Override it via environment variable if needed.

Without the GeoIP database, link redirects still work — geographic data will simply be empty.

## Deployment (Railway / Render)

1. **Set environment variables** on your platform:
   - `SECRET_KEY` — generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DATABASE_URL` — auto-provided by Railway PostgreSQL plugin
   - `DJANGO_SETTINGS_MODULE` — `config.settings.production`
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — `pikolink.com,www.pikolink.com`
   - `EMAIL_HOST_USER` — your SMTP email
   - `EMAIL_HOST_PASSWORD` — your SMTP app password

2. **The Procfile is already configured:**
   ```
   web: gunicorn config.wsgi:application --workers 2 --threads 4 --bind 0.0.0.0:$PORT
   ```

3. **Post-deployment checklist:**
   - Run `python manage.py migrate`
   - Run `python manage.py collectstatic --noinput`
   - Create the first super admin user (see below)
   - Upload `GeoLite2-City.mmdb` to the `geoip/` directory
   - Point DNS to your Railway/Render domain
   - Enable HTTPS in the platform dashboard
   - Test a link creation and redirect end-to-end

## Creating the First Super Admin

```bash
python manage.py shell -c "
from apps.accounts.models import CustomUser
user = CustomUser.objects.get(email='your-email@example.com')
user.is_staff = True
user.is_superuser = True
user.save()
print(f'{user.email} is now a super admin')
"
```

Or use the bootstrap management command if available:

```bash
python manage.py bootstrap_admin --email=admin@pikolink.com --password=changeme
```

The super admin panel is accessible at `/super-admin/` (separate from Django's `/django-admin/`).
