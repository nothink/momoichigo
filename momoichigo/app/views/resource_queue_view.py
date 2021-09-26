"""momoichigo views."""
from __future__ import annotations

from rest_framework import viewsets

from momoichigo.app import models, serializers


class ResourceQueueViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoints for resource_queues.

    Allow: List(Get), Retrieve(Get)
    """

    queryset = models.ResourceQueue.objects.all().order_by("resource")
    serializer_class = serializers.ResourceQueueSerializer
