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
        """Test that __str__  and key is valid."""
        url_str = sources[random.randrange(len(sources))]

        m = models.ResourceQueue.objects.create(source=url_str)

        assert m.__str__() == url_str
