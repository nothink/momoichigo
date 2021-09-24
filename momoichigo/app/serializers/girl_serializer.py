"""serializers."""

from rest_framework import serializers

from momoichigo.app import models


class GirlSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Girl models."""

    class Meta:
        """Meta class for GirlSerializer."""

        model = models.Girl
        fields = ["number", "name"]
