"""serializers."""

from rest_framework import serializers

from momoichigo.app.models import Resource


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Resource models."""

    class Meta:
        """Meta class for ResourceSerializer."""

        model = Resource
        fields = ["source"]
