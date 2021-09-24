"""Girl models."""
from __future__ import annotations

from django.db import models

from .girl import Girl


class Scene(models.Model):
    """Scene models.

    fields:
        number: Scene's Number
        name: Scene's Name
        girl: Scene's Girl
    """

    number = models.PositiveSmallIntegerField(primary_key=True, auto_created=False)
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    girl = models.ForeignKey(Girl, on_delete=models.CASCADE)

    def __str__(self: Scene) -> str:
        """Return desscriptive string."""
        return self.name
