from .base import *

import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['pikolink.com', 'www.pikolink.com', '.railway.app', '.onrender.com']

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
