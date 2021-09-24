"""serializers."""

from rest_framework import serializers

from momoichigo.app import models


class SceneSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Scene models."""

    class Meta:
        """Meta class for SceneSerializer."""

        model = models.Scene
        fields = ["number", "name"]
