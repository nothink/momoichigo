"""Config for All pytest fixtures."""

from typing import Union

import pytest
from django.db.models import Model
from model_bakery import baker
from rest_framework.test import APIRequestFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def factory() -> APIRequestFactory:
    """Fixture for Returning APIRequestFactory."""
    return APIRequestFactory()


@pytest.fixture
def resource() -> Union[list[Model], Model]:
    """Bake a resource."""
    SRC = "https://dqx9mbrpz1jhx.cloudfront.net/vcard/ratio20/images/card/8057cc6ab01af36fea16ccc4952ee910.jpg"  # noqa: E501

    bakes = baker.make("app.Resource", source=SRC)
    return bakes
