"""models."""

from django.db import models


class Resource(models.Model):
    """Resource models."""

    source = models.URLField(unique=True)

    def __str__(self: object) -> str:
        """Return desscriptive string."""
        return super().__str__()
