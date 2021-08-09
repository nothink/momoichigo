"""Resource signals."""

import io
import logging
import urllib.request
from typing import Any, Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from momoichigo.app import models

logger = logging.getLogger(__name__)


@receiver(post_save, sender=models.Resource)
def fetch_and_upload_resource(
    sender: Type[models.Resource],
    instance: models.Resource,
    created: bool,
    **kwargs: Any,
) -> None:
    """作成されたリソースをもとにリソース回収をはかり、GCSのbucketに格納する

    sa: https://docs.djangoproject.com/ja/3.2/ref/signals/#post-save
    """

    if not created:
        return
    # TODO: asyncio を使う
    try:
        # urllib.request を使って fetch
        req = urllib.request.Request(instance.source)
        with urllib.request.urlopen(req) as res:
            body = res.read()
        buf = io.BytesIO(body)
        buf.seek(0)
        instance.file.save(instance.key, buf)

        logger.info("[fetch] " + instance.source)
    except Exception as e:
        # ログだけ出す
        logger.error("[fetch failed] " + instance.source)
        logger.error(e)
