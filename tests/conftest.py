"""Config for All pytest fixtures."""

from typing import Union

import pytest
from django.db.models import Model
from model_bakery import baker
from rest_framework.test import APIRequestFactory

pytestmark = pytest.mark.django_db

SOURCE_PATHS = [
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/ratio20/images/card/8057cc6ab01af36fea16ccc4952ee910.jpg",  # noqa: E501
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/ratio20/images/card/mypage/92469f02bbbaf3ed1c09f2ac03c2228f.jpg",  # noqa: E501
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/mp3/4925/1010_0c08ce73-7036-406a-b2fd-7b46bcc1ed00.mp3",  # noqa: E501
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/mp3/4998/MYPAGE_b5235781-5a3e-469e-b722-e288db1401df.mp3",  # noqa: E501
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/mp3/4998/MYPAGE_6a7839f5-8820-48c4-a452-1119693683d5.mp3",  # noqa: E501
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/mp3/4998/MYPAGE_92ebd462-57da-4727-9bc7-a3260ac09aeb.mp3",  # noqa: E501
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/audio/voice/scenario/atlas/0b5d62c4dbf109d549153fb543078fa7/sprite.mp3",  # noqa: E501
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/ratio20/images/scenario/girl/800x960/2_NuWTUqsW/girl_1.png",  # noqa: E501
    "https://dqx9mbrpz1jhx.cloudfront.net/vcard/ratio20/images/precious/l/987617ec184d2e1f50ab3d8f738ea395.jpg",  # noqa: E501
]


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
