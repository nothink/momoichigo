"""app."""

from django.apps import AppConfig


class AppConfig(AppConfig):
    """App config for momoichigo."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "momoichigo.app"
