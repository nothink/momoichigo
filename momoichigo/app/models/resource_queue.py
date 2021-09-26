"""Resource Queue models."""
from __future__ import annotations

from django.db import models

from .resource import Resource


class ResourceQueue(models.Model):
    """Resource Queue models.

    fields:
        resource: URL of original sources
    """

    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self: ResourceQueue) -> str:
        """Return desscriptive string."""
        return self.resource.source
