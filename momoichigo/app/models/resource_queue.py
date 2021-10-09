"""Resource Queue models."""
from __future__ import annotations

from django.db import models


class ResourceQueue(models.Model):
    """Resource models.

    fields:
        source: URL of original sources
    """

    source = models.URLField(
        null=False,
        blank=False,
        max_length=1024,
    )

    def __str__(self: ResourceQueue) -> str:
        """Return desscriptive string."""
        return self.source
