"""Fetch thread class."""
from __future__ import annotations

import io
import logging
import threading
from typing import Any

import requests

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
        res = requests.get(self.resource.source)
        if res.status_code == 200 and len(res.content) > 0:
            self.resource.file.save(self.resource.key, io.BytesIO(res.content))
            logger.info("[fetch] " + self.resource.source)
        else:
            logger.error(f"[fetch failed: {res.status_code}] {res.url}")
