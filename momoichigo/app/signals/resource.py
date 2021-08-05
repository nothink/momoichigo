"""Resource signals."""

import io
import urllib.request

from django.db.models.signals import post_save
from django.dispatch import receiver

from momoichigo.app import models


@receiver(post_save, sender=models.Resource)
def fetch_and_upload_resource(
    sender, instance: models.Resource, created: bool, **kwargs
):
    """
    作成されたリソースをもとにリソース回収をはかり、GCSのbucketに格納する
    sa: https://docs.djangoproject.com/ja/3.2/ref/signals/#post-save
    """

    if not created:
        return

    try:
        print(sender)
        req = urllib.request.Request(instance.source)
        with urllib.request.urlopen(req) as res:
            body = res.read()
        buf = io.BytesIO(body)
        buf.seek(0)
        instance.file.save("tmp.jpg", buf)
    except Exception as e:
        # TODO: なんらかのログを吐くべき
        print(e)
