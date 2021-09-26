"""serializers."""

from rest_framework import serializers

from momoichigo.app import models


class ResourceQueueSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Resource Queue models."""

    class Meta:
        """Meta class for ResourceQueueSerializer."""

        model = models.ResourceQueue
        fields = ["resource"]
