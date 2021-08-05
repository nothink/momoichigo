"""models."""
from __future__ import annotations

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
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self: Resource) -> str:
        """Return desscriptive string."""
        return self.source
