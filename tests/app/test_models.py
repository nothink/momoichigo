"""tests for models."""
from __future__ import annotations

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

    def test_model_has_valid_str(self: TestResource) -> None:
        """Test that __str__ is valid."""
        emi_url = "/".join(["https://dqx9mbrpz1jhx.cloudfront.net", self.EMI_KEY])

        m = models.Resource.objects.create(source=emi_url)
        # signals上のスレッドがFetchし終わるまで sleep()

        assert m.__str__() == emi_url
        assert m.key == self.EMI_KEY
