"""Tests for View and ViewSets."""
# https://dev.to/sherlockcodes/pytest-with-django-rest-framework-from-zero-to-hero-8c4#viewsets

from __future__ import annotations

import json
from typing import Union

import pytest
from django.db.models import Model
from rest_framework.test import APIRequestFactory

from momoichigo.app.views import ResourceViewSet

pytestmark = pytest.mark.django_db


class TestResourceEndpoints:
    """Tests for '/resources' ."""

    endpoint = "/api/resources/"

    def test_list_resources_ok(
        self: TestResourceEndpoints,
        factory: APIRequestFactory,
        resource: Union[list[Model], Model],
    ) -> None:
        """Test for list (GET)."""
        SRC = "https://dqx9mbrpz1jhx.cloudfront.net/vcard/ratio20/images/card/8057cc6ab01af36fea16ccc4952ee910.jpg"  # noqa: E501

        request = factory.get(self.endpoint)
        response = ResourceViewSet.as_view({"get": "list"})(request)

        assert response.status_code == 200

        response.render()
        response_body = json.loads(response.content)

        assert response_body["count"] == 1
        assert response_body["next"] is None
        assert response_body["previous"] is None
        assert response_body["results"][0]["source"] == SRC
