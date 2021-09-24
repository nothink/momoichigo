"""tests for models."""
from __future__ import annotations

import random
from urllib.parse import urlparse

import pytest

from momoichigo.app import models

pytestmark = pytest.mark.django_db


class TestResource:
    """Test Unit of Resource models."""

    @staticmethod
    def test_model_has_valid_str(sources: list[str]) -> None:
        """Test that __str__  and key is valid."""
        url_str = sources[random.randrange(len(sources))]
        url = urlparse(url_str)

        m = models.Resource.objects.create(source=url_str)
        # signals上のスレッドがFetchし終わるまで sleep()

        assert m.__str__() == url_str
        assert m.key == url.path[1:]


class TestGirl:
    """Test Unit of Girl models."""

    @staticmethod
    def test_model_has_valid_str() -> None:
        """Test that __str__  and key is valid."""
        TOMTOM = "戸村美知留"

        m = models.Girl.objects.create(name=TOMTOM)
        # signals上のスレッドがFetchし終わるまで sleep()

        assert m.__str__() == TOMTOM
