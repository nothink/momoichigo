"""Resource signals."""

from typing import Any, Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from momoichigo.app import models


@receiver(post_save, sender=models.Resource)
def add_resource_queue(
    sender: Type[models.Resource],
    instance: models.Resource,
    created: bool,
    **kwargs: Any,
) -> None:
    """Add this resource into Queue.

    sa: https://docs.djangoproject.com/ja/3.2/ref/signals/#post-save
    """
    if created:
        # Resource Queue に追加
        models.ResourceQueue.objects.create(resource=instance)
