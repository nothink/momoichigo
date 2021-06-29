"""tests for models."""

import pytest

from momoichigo.app import models


@pytest.mark.django_db
def test_model_has_valid_str() -> None:
    """Test that __str__ is valid."""
    emi_path = "/".join(
        [
            "https://dqx9mbrpz1jhx.cloudfront.net",
            "vcard",
            "ratio20",
            "images",
            "card",
            "527b0285dc0532c9da390f14cc8954fe.jpg",
        ]
    )
    m = models.Resource.objects.create(source=emi_path)
    assert m.__str__() == emi_path
