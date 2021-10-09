"""serializers."""
from __future__ import annotations

from typing import Any

from rest_framework import serializers

from momoichigo.app import models


class ResourceQueueListSerializer(serializers.ListSerializer):
    """ListSerializer for ResourceQueue."""

    def create(
        self: ResourceQueueListSerializer, validated_data: list[Any]
    ) -> list[Any]:
        """Create multiple models."""
        queues = [models.ResourceQueue(**item) for item in validated_data]
        return models.ResourceQueue.objects.bulk_create(queues)

    def update(
        self: ResourceQueueListSerializer,
        instances: list[Any],
        validated_data: list[Any],
    ) -> list[Any]:
        """Update is not implemented."""
        raise NotImplementedError("ResourceQueue is not able to update.")


class ResourceQueueSerializer(serializers.ModelSerializer):
    """Serializer for ResourceQueue models."""

    class Meta:
        """Meta class for ResourceQueueSerializer."""

        model = models.ResourceQueue
        fields = ["source"]
        list_serializer_class = ResourceQueueListSerializer
