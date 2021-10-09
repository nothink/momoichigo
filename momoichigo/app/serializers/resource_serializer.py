"""serializers."""

from rest_framework import serializers

from momoichigo.app import models


class ResourceSerializer(serializers.ModelSerializer):
    """Serializer for Resource models."""

    class Meta:
        """Meta class for ResourceSerializer."""

        model = models.Resource
        fields = "__all__"
