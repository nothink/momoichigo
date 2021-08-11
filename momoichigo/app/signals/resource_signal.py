"""Resource signals."""

from typing import Any, Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from momoichigo.app import models

from .threading import fetcher


@receiver(post_save, sender=models.Resource)
def fetch_and_upload_resource(
    sender: Type[models.Resource],
    instance: models.Resource,
    created: bool,
    **kwargs: Any,
) -> None:
    """Fetc and upload resources.

        作成されたリソースをもとにリソース回収をはかり、GCSのbucketに格納する
    sa: https://docs.djangoproject.com/ja/3.2/ref/signals/#post-save
    """
    if created:
        # Fetch thread を立ち上げて開始、投げっぱなし
        fetcher.Fetcher(instance).start()
