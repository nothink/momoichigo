"""Fetch thread class."""
from __future__ import annotations

import io
import logging
import threading
import urllib.request
from typing import Any

from momoichigo.app import models

logger = logging.getLogger(__name__)


class Fetcher(threading.Thread):
    """Fetcher class.

    sa: https://stackoverflow.com/questions/11899088/
    """

    def __init__(self: Fetcher, resource: models.Resource, **kwargs: Any) -> None:
        """Init."""
        self.resource = resource
        super(Fetcher, self).__init__(**kwargs)

    def run(self: Fetcher) -> None:
        """Run threads."""
        try:
            # urllib.request を使って fetch
            req = urllib.request.Request(self.resource.source)
            with urllib.request.urlopen(req) as res:
                body = res.read()
            buf = io.BytesIO(body)
            buf.seek(0)
            self.resource.file.save(self.resource.key, buf)

            logger.info("[fetch] " + self.resource.source)
        except Exception as e:
            # ログだけ出す
            logger.error("[fetch failed] " + self.resource.source)
            logger.error(e)
