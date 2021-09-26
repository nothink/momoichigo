"""Tests for ResourceViewSet."""
from __future__ import annotations

import json
import random
from typing import Any

import pytest
from rest_framework.test import APIRequestFactory

from momoichigo.app.views import ResourceViewSet

pytestmark = pytest.mark.django_db


class TestResourceView:
    """Tests for '/resources/' ."""

    endpoint = "/api/resources/"

    def test_list_resources_ok(
        self: TestResourceView,
        factory: APIRequestFactory,
        sources: list[str],
        resources: list[Any],
    ) -> None:
        """Test for list (GET)."""
        request = factory.get(self.endpoint)
        response = ResourceViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 200

        response.render()
        response_body = json.loads(response.content)

        assert response_body["count"] == len(resources)
        assert response_body["results"][0]["source"] == sources[0]

    def test_retrieve_resources_ok(
        self: TestResourceView,
        client: Any,
        resources: list[Any],
    ) -> None:
        """Test for retrieve (GET)."""
        item = resources[random.randrange(len(resources))]
        expected_json = {}
        expected_json["created"] = item.created.astimezone().isoformat()
        expected_json["file"] = None
        expected_json["source"] = item.source

        response = client.get(f"{self.endpoint}{item.id}/")

        assert response.status_code in [200, 301]

        response_body = json.loads(response.content)

        assert response_body == expected_json

    def test_create_one_resource_ok(
        self: TestResourceView,
        client: Any,
        sources: list[str],
    ) -> None:
        """Test for create one (POST)."""
        url_str = sources[random.randrange(len(sources))]
        request_dict = {"source": url_str}

        response = client.post(self.endpoint, request_dict, format="json")

        assert response.status_code == 201

        response_body = json.loads(response.content)

        assert response_body == [url_str]

    def test_create_multi_resource_ok(
        self: TestResourceView,
        client: Any,
        sources: list[str],
    ) -> None:
        """Test for create multi (POST)."""
        request_dict = []
        for source in sources:
            item = {"source": source}
            request_dict.append(item)

        response = client.post(self.endpoint, request_dict, format="json")

        assert response.status_code == 201

        response_body = json.loads(response.content)

        assert response_body == sources

    def test_create_duplicate_one_resource_ok(
        self: TestResourceView,
        client: Any,
        sources: list[str],
        resources: list[Any],
    ) -> None:
        """Test for create duplicated one (POST)."""
        url_str = sources[random.randrange(len(sources))]
        request_dict = {"source": url_str}

        response = client.post(self.endpoint, request_dict, format="json")

        assert response.status_code == 204

        assert response.content == b""

    def test_create_duplicate_another_resource_ok(
        self: TestResourceView,
        client: Any,
        sources: list[str],
    ) -> None:
        """Test for create duplicated another (POST)."""
        # create one
        url_str = sources[random.randrange(len(sources))]
        request_one_dict = {"source": url_str}

        response = client.post(self.endpoint, request_one_dict, format="json")

        another_dict = []
        for source in sources:
            item = {"source": source}
            another_dict.append(item)

        response = client.post(self.endpoint, another_dict, format="json")

        assert response.status_code == 201

        response_body = json.loads(response.content)

        assert len(response_body) == len(another_dict) - 1
        assert url_str not in response_body
