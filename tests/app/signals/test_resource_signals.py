"""tests for signals."""
from __future__ import annotations

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
        post_save.send(
            models.Resource,
            instance=single_resource,
            created=False,
        )
        queues = models.ResourceQueue.objects.filter(resource=single_resource)

        assert len(queues) == 1
