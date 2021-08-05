"""app."""
from __future__ import annotations

from django.apps import AppConfig


class AppConfig(AppConfig):
    """App config for momoichigo."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "momoichigo.app"

    def ready(self: AppConfig) -> None:
        """When called the application is ready."""
        # importing signals
        from . import signals  # noqa: F401
