"""Tests for ResourceQueueViewSet."""

from __future__ import annotations

import random
import shutil
from typing import Any

import pytest
from rest_framework.test import APIRequestFactory

from momoichigo.app.models import Resource, ResourceQueue
from momoichigo.app.views import ResourceQueueViewSet

pytestmark = pytest.mark.django_db


class TestResourceQueueView:
    """Tests for '/resource_queues/' ."""

    endpoint = "/api/resource_queues/"

    def test_list_empty_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
    ) -> None:
        """Test for list empty (GET)."""
        assert len(ResourceQueue.objects.all()) == 0

        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 204
        assert len(ResourceQueue.objects.all()) == 0

    def test_list_single_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
        resources: list[Any],
    ) -> None:
        """Test for list single (GET)."""
        item = resources[random.randrange(len(resources))]
        ResourceQueue.objects.create(resource=item)

        for resource in Resource.objects.all():
            assert bool(resource.file) is False

        # signals を止めているので、Queueはこれのみのはず
        assert len(ResourceQueue.objects.all()) == 1

        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 202
        # Queueに残りが格納されていること
        assert len(ResourceQueue.objects.all()) == len(resources) - 1

        # clean up local checked files.
        shutil.rmtree(item.key.split("/")[0])

    def test_list_multi_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
        resources: list[Any],
    ) -> None:
        """Test for list multi (GET)."""
        # 2 から len(resources)-1 件のいずれかでテスト
        multi_length = random.randint(2, len(resources) - 1)
        for item in resources:
            if len(ResourceQueue.objects.all()) >= multi_length:
                break
            ResourceQueue.objects.create(resource=item)

        for resource in Resource.objects.all():
            assert bool(resource.file) is False

        # signals を止めているので、Queueはこれらのみのはず
        assert len(ResourceQueue.objects.all()) == multi_length

        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 202
        # Queueに残りが格納されていること
        assert len(ResourceQueue.objects.all()) == len(resources) - multi_length
        for queue in ResourceQueue.objects.all():
            assert bool(queue.resource.file) is False

        # clean up local checked files.
        shutil.rmtree(resources[0].key.split("/")[0])

    def test_second_list_queue_ok(
        self: TestResourceQueueView,
        factory: APIRequestFactory,
        resources: list[Any],
    ) -> None:
        """Test for list multi (GET)."""
        # 2 から len(resources)-1 件のいずれかでテスト
        multi_length = random.randint(2, len(resources) - 1)
        for item in resources:
            if len(ResourceQueue.objects.all()) >= multi_length:
                break
            ResourceQueue.objects.create(resource=item)

        for resource in Resource.objects.all():
            assert bool(resource.file) is False

        # signals を止めているので、Queueはこれらのみのはず
        assert len(ResourceQueue.objects.all()) == multi_length

        # 1回目
        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 202
        # Queueに残りが格納されていること
        assert len(ResourceQueue.objects.all()) == len(resources) - multi_length
        for queue in ResourceQueue.objects.all():
            assert bool(queue.resource.file) is False

        # 1回目
        request = factory.get(self.endpoint)
        response = ResourceQueueViewSet.as_view({"get": "list"})(request)
        assert response.status_code == 202
        # Queueが空のこと
        assert len(ResourceQueue.objects.all()) == 0

        # clean up local checked files.
        shutil.rmtree(resources[0].key.split("/")[0])
