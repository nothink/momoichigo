"""tests for models."""
from __future__ import annotations

import os
import shutil
import time

import pytest

from momoichigo import settings
from momoichigo.app import models


class TestResource:
    """Test Unit of Resource models."""

    @pytest.mark.django_db()
    def test_model_has_valid_str(self: TestResource) -> None:
        """Test that __str__ is valid."""
        emi_key = "/".join(
            [
                "vcard",
                "ratio20",
                "images",
                "card",
                "527b0285dc0532c9da390f14cc8954fe.jpg",
            ]
        )
        emi_url = "/".join(["https://dqx9mbrpz1jhx.cloudfront.net", emi_key])
        m = models.Resource.objects.create(source=emi_url)
        # signals上のスレッドがFetchし終わるまで sleep()
        time.sleep(3)
        assert m.__str__() == emi_url
        assert m.key == emi_key
        assert m.file.path == os.path.abspath(emi_key)
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, "vcard"))
