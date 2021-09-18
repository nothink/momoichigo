"""tests for models."""
from __future__ import annotations

from urllib.parse import urlparse

import pytest

from momoichigo.app import models

pytestmark = pytest.mark.django_db


class TestResource:
    """Test Unit of Resource models."""

    # valid URL
    EMI_KEY = "/".join(
        [
            "vcard",
            "ratio20",
            "images",
            "card",
            "527b0285dc0532c9da390f14cc8954fe.jpg",
        ]
    )

    def test_model_has_valid_str(self: TestResource, sources: list[str]) -> None:
        """Test that __str__ is valid."""
        target_url = sources[0]
        url = urlparse(target_url)

        m = models.Resource.objects.create(source=target_url)
        # signals上のスレッドがFetchし終わるまで sleep()

        assert m.__str__() == target_url
        assert m.key == url.path[1:]
