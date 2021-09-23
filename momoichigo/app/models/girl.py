"""Girl models."""
from __future__ import annotations

from django.db import models


class Girl(models.Model):
    """Girl models.

    fields:
        name: Girl's Name
    """

    name = models.CharField(max_length=50)

    def __str__(self: Girl) -> str:
        """Return desscriptive string."""
        return self.name
