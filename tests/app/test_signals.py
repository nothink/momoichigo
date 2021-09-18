"""tests for signals."""
from __future__ import annotations

import shutil
import time
from typing import Any

import pytest
from django.db.models.signals import post_save

from momoichigo.app import models

# https://dev.to/sherlockcodes/pytest-with-django-rest-framework-from-zero-to-hero-8c4#signals # noqa

# see also: https://www.cameronmaske.com/muting-django-signals-with-a-pytest-fixture/
pytestmark = [pytest.mark.enable_signals, pytest.mark.django_db]


class TestResourceSignal:
    """tests for signals."""

    @staticmethod
    def test_post_save(single_resource: Any) -> None:
        """Testing signals for post_save Resource instance."""
        instance = single_resource

        # Wait for downloading.
        time.sleep(3)
        assert instance.file.name == instance.key

        post_save.send(
            models.Resource,
            instance=instance,
            created=False,
        )
        assert instance.file.name == instance.key

        # clean up local checked files.
        shutil.rmtree(instance.key.split("/")[0])
