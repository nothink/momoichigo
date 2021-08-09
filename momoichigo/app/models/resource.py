"""models."""
from __future__ import annotations

from urllib.parse import urlparse

from django.core.validators import RegexValidator
from django.db import models


class Resource(models.Model):
    """Resource models.

    fields:
        source: URL of original sources
        created: created timestamp
    """

    # validator: the source url is a resources at https://vcard.ameba.jp/
    validate_vcard_host = RegexValidator(
        regex=r"^http(s)?://dqx9mbrpz1jhx.cloudfront.net/vcard/.*",
        message=("This url isn't a valid url of the 'vcard' resources"),
    )

    source = models.URLField(
        unique=True,
        null=False,
        blank=False,
        validators=[validate_vcard_host],
        max_length=1024,
    )
    # sa: https://docs.djangoproject.com/ja/3.2/topics/files/
    # sa: https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html#model
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self: Resource) -> str:
        """Return desscriptive string."""
        return self.source

    @property
    def key(self: Resource) -> str:
        """Return key from source url."""
        url = urlparse(self.source)
        return url.path[1:]
