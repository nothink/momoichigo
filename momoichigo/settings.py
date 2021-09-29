"""
Django settings for momoichigo project.

sa: https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import io
import os
from pathlib import Path
from typing import Any

import environ
import google.auth
import google.cloud.logging
from django.utils.crypto import get_random_string
from google.cloud.secretmanager import SecretManagerServiceClient

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = os.path.join(BASE_DIR, ".env")

# Get temporary SECRET_KEY for no environs
__CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)"
__TMP_SECRET_KEY = get_random_string(50, __CHARS)

# Django environ
env = environ.Env(
    DEV=(bool, False),
    TZ=(str, "UTC"),
    SECRET_KEY=(str, __TMP_SECRET_KEY),
    DATABASE_URL=(str, "sqlite:////tmp/db.sqlite3"),
    ALLOWED_HOSTS=(list, []),
    RUNTIME=(str, "local"),
    GS_BUCKET_NAME=(str, "bucket"),
    SLACK_API_TOKEN=(str, ""),
)

# -------- cloudrun_django_secret_config --------
# https://cloud.google.com/python/django/run#understand_the_code
# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, proj = google.auth.default()
    if isinstance(proj, str):
        os.environ["GOOGLE_CLOUD_PROJECT"] = proj
except google.auth.exceptions.DefaultCredentialsError:  # type: ignore
    pass

if os.path.isfile(env_file):
    # Use a local secret file, if provided ".env"
    env.read_env(env_file)
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    version = client.access_secret_version(name=name)  # type: ignore
    payload = version.payload.data.decode("UTF-8")
    env.read_env(io.StringIO(payload))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEV")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "momoichigo.app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "momoichigo.urls"

CORS_ALLOWED_ORIGINS = [
    "https://vcard.ameba.jp",
]
CORS_ALLOW_CREDENTIALS = True

REST_FRAMEWORK = {
    # sa: https://www.django-rest-framework.org/api-guide/pagination/
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 1000,
    "DEFAULT_RENDERER_CLASSES": [
        # Renderers
        # https://www.django-rest-framework.org/api-guide/renderers/
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "momoichigo.wsgi.application"


# Database
# https://django-environ.readthedocs.io/en/latest/
DATABASES: dict[str, dict[str, Any]] = {"default": env.db()}
# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

USE_TZ = True
TIME_ZONE = env("TZ")

USE_I18N = False
USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if env("RUNTIME") == "gcp":
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "cloud_logging": {
                "class": "google.cloud.logging.handlers.CloudLoggingHandler",
                "client": google.cloud.logging.Client(),
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["cloud_logging"],
                "level": "INFO",
            },
        },
    }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
                "propagate": False,
            },
        },
    }

# https://docs.djangoproject.com/ja/3.2/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# storage
if env("RUNTIME") == "gcp":
    # Google Cloud Storage using django-storages
    # https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

    GS_BUCKET_NAME = env("GS_BUCKET_NAME")
    GS_DEFAULT_ACL = "publicRead"
    GS_FILE_OVERWRITE = True
    GS_MAX_MEMORY_SIZE = 134217728

elif env("RUNTIME") == "local":
    MEDIA_ROOT = str(BASE_DIR)

SLACK_API_TOKEN: str = env("SLACK_API_TOKEN")  # type: ignore
