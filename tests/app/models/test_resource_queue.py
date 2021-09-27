"""tests for models."""
from __future__ import annotations

import random

import pytest

from momoichigo.app import models

pytestmark = pytest.mark.django_db


class TestResourceQueue:
    """Test Unit of ResourceQueue models."""

    @staticmethod
    def test_model_has_valid_str(sources: list[str]) -> None:
        """Test that __str__  is valid."""
        url_str = sources[random.randrange(len(sources))]

        r = models.Resource.objects.create(source=url_str)
        m = models.ResourceQueue.objects.create(resource=r)

        assert m.__str__() == url_str
