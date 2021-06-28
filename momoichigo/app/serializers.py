"""serializers."""

from rest_framework import serializers

from momoichigo.app.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    """Serializer for Resource models.

    sa: https://github.com/miki725/django-rest-framework-bulk
    """

    class Meta:
        """Meta class for ResourceSerializer."""

        model = Resource
        fields = ["source"]
