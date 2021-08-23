"""app."""
from __future__ import annotations

from django.apps import AppConfig


class IchigoAppConfig(AppConfig):
    """App config for momoichigo."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "momoichigo.app"

    def ready(self: IchigoAppConfig) -> None:
        """When called the application is ready."""
        # importing signals
        from . import signals  # noqa: F401
