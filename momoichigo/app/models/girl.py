"""Girl models."""
from __future__ import annotations

from django.db import models


class Girl(models.Model):
    """Girl models.

    fields:
        number: Girl's student number
        name: Girl's Name
    """

    number = models.PositiveSmallIntegerField(primary_key=True, auto_created=False)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)

    def __str__(self: Girl) -> str:
        """Return desscriptive string."""
        return self.name
