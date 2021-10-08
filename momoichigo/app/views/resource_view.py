"""momoichigo views."""
from __future__ import annotations

from rest_framework import viewsets

from momoichigo.app import models, serializers


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """リソース表示用のViewSet.

    Allow: List(Get), Retrieve(Get)
    """

    queryset = models.Resource.objects.all().order_by("source")
    serializer_class = serializers.ResourceSerializer
