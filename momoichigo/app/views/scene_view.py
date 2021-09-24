"""momoichigo views."""
from rest_framework import viewsets

from momoichigo.app import models, serializers


class SceneViewSet(viewsets.ModelViewSet):
    """api endpoints for resource."""

    queryset = models.Scene.objects.all()
    serializer_class = serializers.SceneSerializer
    # permission_classes = [permissions.IsAuthenticated]
