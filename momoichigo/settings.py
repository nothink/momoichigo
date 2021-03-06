"""
Django settings for momoichigo project.

sa: https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from typing import Any

import environ
from django.utils.crypto import get_random_string

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = os.path.join(BASE_DIR, ".env")

# Get temporary SECRET_KEY for no environs
__CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)"
__TMP_SECRET_KEY = get_random_string(50, __CHARS)

# Django environ
env = environ.Env(
    DEBUG=(bool, False),
    TZ=(str, "UTC"),
    SECRET_KEY=(str, __TMP_SECRET_KEY),
    DATABASE_URL=(str, "sqlite:////tmp/db.sqlite3"),
    ALLOWED_HOSTS=(list, []),
    RUNTIME=(str, "local"),
    GS_BUCKET_NAME=(str, "bucket"),
    SLACK_API_TOKEN=(str, ""),
)

if os.path.isfile(env_file):
    # Use a local secret file, if provided ".env"
    env.read_env(env_file)

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.twitter",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "momoichigo.app",
]
SITE_ID = 1

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
    "https://seio.club",
    "https://api.seio.club",
    "https://vcard.ameba.jp",
    "https://dqx9mbrpz1jhx.cloudfront.net",
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    "seio.club",
    "api.seio.club",
    "vcard.ameba.jp",
    "dqx9mbrpz1jhx.cloudfront.net",
]

REST_FRAMEWORK = {
    # sa: https://www.django-rest-framework.org/api-guide/pagination/
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 1000,
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        # Renderers
        # https://www.django-rest-framework.org/api-guide/renderers/
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
}
if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.AdminRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ]

REST_USE_JWT = True
JWT_AUTH_COOKIE = "momoichigo-auth"
JWT_AUTH_REFRESH_COOKIE = "momoichigo-refresh-token"

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
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "app_cache",
    }
}

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

# https://docs.djangoproject.com/ja/3.2/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
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
