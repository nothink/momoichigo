"""momoichigo views."""
from rest_framework import viewsets

from momoichigo.app import models, serializers


class GirlViewSet(viewsets.ModelViewSet):
    """api endpoints for resource."""

    queryset = models.Girl.objects.all()
    serializer_class = serializers.GirlSerializer
    # permission_classes = [permissions.IsAuthenticated]
