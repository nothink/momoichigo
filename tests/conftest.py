"""Config for All pytest fixtures."""

import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def factory() -> APIRequestFactory:
    return APIRequestFactory()
