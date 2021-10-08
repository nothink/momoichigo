"""Tests for ResourceViewSet."""
from __future__ import annotations

import json
import random
from typing import Any

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from momoichigo.app import views
from momoichigo.settings import TIME_ZONE

pytestmark = pytest.mark.django_db


class TestResourceView:
    """Tests for '/resources/' endpoint View."""

    def test_list_resources_ok(
        self: TestResourceView,
        factory: APIRequestFactory,
        sources: list[str],
        resources: list[Any],
    ) -> None:
        """Test for list (GET)."""
        request = factory.get(reverse("resource-list"))
        response = views.ResourceViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 200

        response.render()
        response_body = json.loads(response.content)

        assert response_body["count"] == len(resources)
        for i in range(len(resources)):
            assert response_body["results"][i]["source"] == sorted(sources)[i]

    def test_retrieve_resources_ok(
        self: TestResourceView,
        factory: APIRequestFactory,
        resources: list[Any],
    ) -> None:
        """Test for retrieve (GET)."""
        item = resources[random.randrange(len(resources))]
        expected_json = {}
        if TIME_ZONE == "UTC":
            # UTCのときはPythonのisoformat()だとZ形式で出てくれないので手作業修正
            expected_json["created"] = item.created.isoformat()[:-6] + "Z"
            expected_json["modified"] = item.modified.isoformat()[:-6] + "Z"
        else:
            expected_json["created"] = item.created.astimezone().isoformat()
            expected_json["modified"] = item.modified.astimezone().isoformat()
        expected_json["id"] = item.id
        expected_json["file"] = None
        expected_json["source"] = item.source

        # retrieve のURLはこちら参照
        # https://www.django-rest-framework.org/api-guide/routers/#defaultrouter
        request = factory.get(reverse("resource-detail", args=[item.id]))
        response = views.ResourceViewSet.as_view({"get": "retrieve"})(
            request, pk=item.id
        )

        assert response.status_code in [200, 301]

        response.render()
        response_body = json.loads(response.content)

        assert response_body == expected_json
