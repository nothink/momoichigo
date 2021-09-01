"""
Django settings for momoichigo project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

import environ
from django.utils.crypto import get_random_string
from google.oauth2 import service_account

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Get temporary SECRET_KEY for no environs
__CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)"
__TMP_SECRET_KEY = get_random_string(50, __CHARS)

# Django environ
env = environ.Env(
    DEV=(bool, True),
    SECRET_KEY=(str, __TMP_SECRET_KEY),
    ALLOWED_HOSTS=(list, []),
    STORAGE_TYPE=(str, "local"),
    GS_CREDENTIALS=(str, "/cred.json"),
    GS_BUCKET_NAME=(str, "bucket"),
    GS_PROJECT_ID=(str, "project"),
)
env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

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
    "rest_framework",
    "momoichigo.app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "momoichigo.urls"

REST_FRAMEWORK = {
    # sa: https://www.django-rest-framework.org/api-guide/pagination/
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 1000,
    # "DEFAULT_AUTHENTICATION_CLASSES": (
    #     "rest_framework_simplejwt.authentication.JWTAuthentication",
    # ),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
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
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# https://django-environ.readthedocs.io/en/latest/#
DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:////tmp/db.sqlite3")}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

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
}

# https://docs.djangoproject.com/ja/3.2/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]


# storage
if env("STORAGE_TYPE") == "gcs":
    # Google Cloud Storage using django-storages
    # https://django-storages.readthedocs.io/en/latest/backends/gcloud.html
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"

    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        env("GS_CREDENTIALS")
    )
    GS_BUCKET_NAME = env.str("GS_BUCKET_NAME")
    GS_LOCATION = ""

    GS_URL = "https://storage.googleapis.com/" + str(GS_BUCKET_NAME)

    MEDIA_ROOT = "/"
    MEDIA_URL = GS_URL + MEDIA_ROOT

    GS_FILE_OVERWRITE = True
    GS_MAX_MEMORY_SIZE = 134217728

elif env("STORAGE_TYPE") == "local":
    MEDIA_ROOT = str(BASE_DIR)
