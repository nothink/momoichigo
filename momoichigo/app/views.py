"""views."""

from rest_framework import viewsets

from momoichigo.app.models import Resource
from momoichigo.app.serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """api endpoints for resource."""

    queryset = Resource.objects.all().order_by("source")
    serializer_class = ResourceSerializer
