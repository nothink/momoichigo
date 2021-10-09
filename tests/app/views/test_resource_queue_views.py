"""Tests for ResourceViewSet."""
from __future__ import annotations

import json
import shutil
from typing import Any
from urllib.parse import urlparse

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from momoichigo.app import models, views

pytestmark = pytest.mark.django_db


class TestResourceQueueView:
    """Tests for '/resources/queues/' endpoint View."""

    @staticmethod
    def test_create_queues_dict_ok(
        factory: APIRequestFactory,
        sources: list[str],
    ) -> None:
        """Test for create (POST) with dict."""
        data = [{"source": x} for x in sources]

        request = factory.post(reverse("resource-queue-list"), data, format="json")
        response = views.ResourceQueueViewSet.as_view({"post": "create"})(request)

        assert response.status_code == status.HTTP_201_CREATED

        response.render()
        response_body = json.loads(response.content)

        assert response_body == data

    @staticmethod
    def test_create_queues_str_ok(
        factory: APIRequestFactory,
        sources: list[str],
    ) -> None:
        """Test for create (POST) with list[str]."""
        expected_data = [{"source": x} for x in sources]

        request = factory.post(reverse("resource-queue-list"), sources, format="json")
        response = views.ResourceQueueViewSet.as_view({"post": "create"})(request)

        assert response.status_code == status.HTTP_201_CREATED

        response.render()
        response_body = json.loads(response.content)

        assert response_body == expected_data

    @staticmethod
    def test_list_queues_empty_ok(
        factory: APIRequestFactory,
    ) -> None:
        """Test for list (GET) normally."""
        request = factory.get(reverse("resource-queue-list"))
        response = views.ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == status.HTTP_200_OK

    @staticmethod
    def test_list_queues_normally_ok(
        factory: APIRequestFactory,
        resource_queues: list[Any],
    ) -> None:
        """Test for list (GET) normally."""
        request = factory.get(reverse("resource-queue-list"))
        response = views.ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == status.HTTP_201_CREATED

        response.render()
        response_body = json.loads(response.content)

        assert len(response_body) == len(resource_queues)
        response_sources = sorted(response_body)
        expected_sources = sorted([q.source for q in resource_queues])
        for i in range(len(resource_queues)):
            assert response_sources[i] == expected_sources[i]

        # clean up
        dir_path = urlparse(response_sources[0]).path
        shutil.rmtree(dir_path.split("/")[1])

    @staticmethod
    def test_list_queues_all_dup_ok(
        factory: APIRequestFactory,
        resources: list[Any],
        resource_queues: list[Any],
    ) -> None:
        """Test for list (GET) when all items are already exist."""
        request = factory.get(reverse("resource-queue-list"))
        response = views.ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == status.HTTP_200_OK

        response.render()
        response_body = json.loads(response.content)

        assert len(response_body) == 0

    @staticmethod
    def test_list_queues_heavy_ok(
        factory: APIRequestFactory,
        heavy_queues: list[Any],
    ) -> None:
        """Test for list (GET) normally."""
        request = factory.get(reverse("resource-queue-list"))
        response = views.ResourceQueueViewSet.as_view({"get": "list"})(request)

        assert response.status_code == status.HTTP_201_CREATED

        response.render()
        response_body = json.loads(response.content)

        remain_queue = models.ResourceQueue.objects.all()

        assert len(response_body) == len(heavy_queues) - len(remain_queue)
        response_sources = sorted(response_body)
        expected_sources = sorted(
            list({q.source for q in heavy_queues} - {q.source for q in remain_queue})
        )
        for i, elem in enumerate(response_sources):
            assert elem == expected_sources[i]

        # clean up
        dir_path = urlparse(response_sources[0]).path
        shutil.rmtree(dir_path.split("/")[1])
