"""serializers."""

from rest_framework import serializers

from momoichigo.app import models


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Resource models."""

    class Meta:
        """Meta class for ResourceSerializer."""

        model = models.Resource
        fields = ["source", "created"]
