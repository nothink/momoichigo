"""Config for All pytest fixtures."""

from typing import Any, Union

import pytest
from django.db.models import Model
from django.db.models.signals import post_save
from model_bakery import baker
from rest_framework.test import APIClient, APIRequestFactory

pytestmark = pytest.mark.django_db

SOURCE_BASE = "https://dqx9mbrpz1jhx.cloudfront.net/vcard/"

SOURCE_PATHS = [
    SOURCE_BASE
    + "audio/voice/scenario/atlas/0b5d62c4dbf109d549153fb543078fa7/sprite.mp3",
    SOURCE_BASE + "mp3/4925/1010_0c08ce73-7036-406a-b2fd-7b46bcc1ed00.mp3",
    SOURCE_BASE + "mp3/4998/MYPAGE_b5235781-5a3e-469e-b722-e288db1401df.mp3",
    SOURCE_BASE + "mp3/4998/MYPAGE_6a7839f5-8820-48c4-a452-1119693683d5.mp3",
    SOURCE_BASE + "mp3/4998/MYPAGE_92ebd462-57da-4727-9bc7-a3260ac09aeb.mp3",
    SOURCE_BASE + "ratio20/images/card/2b387c21824d4aa6bd7519adf6e1530f.jpg",
    SOURCE_BASE + "ratio20/images/card/368663d7936a73985a7b0fdc010d7bb9.jpg",
    SOURCE_BASE + "ratio20/images/card/413535f9464f8ddda9a514c87ba82e6d.jpg",
    SOURCE_BASE + "ratio20/images/card/4f583f313fadcf5e02455e2a8d812c56.jpg",
    SOURCE_BASE + "ratio20/images/card/8057cc6ab01af36fea16ccc4952ee910.jpg",
    SOURCE_BASE + "ratio20/images/card/87e9498c06622875eaa2774f452c9d2c.jpg",
    SOURCE_BASE + "ratio20/images/card/a3d9cb8cff48b1bec8334b8d53eaec2f.jpg",
    SOURCE_BASE + "ratio20/images/card/gif/053d5298bd0e7941b12479c643f19a1e.gif",
    SOURCE_BASE + "ratio20/images/card/gif/0fdec0b58da46363e641eae6b1837c14.gif",
    SOURCE_BASE + "ratio20/images/card/gif/1340b8183a18d608ccfb6fd505b5c8c9.gif",
    SOURCE_BASE + "ratio20/images/card/gif/209bcdf804c598b4546f3ccbe4656c00.gif",
    SOURCE_BASE + "ratio20/images/card/gif/251957cfdb120f467802e1a3888a951a.gif",
    SOURCE_BASE + "ratio20/images/card/gif/2ae7eec12892f9eff6d17abcfc0e3fec.gif",
    SOURCE_BASE + "ratio20/images/card/mypage/92469f02bbbaf3ed1c09f2ac03c2228f.jpg",
    SOURCE_BASE + "ratio20/images/precious/l/987617ec184d2e1f50ab3d8f738ea395.jpg",
    SOURCE_BASE + "ratio20/images/scenario/girl/800x960/2_NuWTUqsW/girl_1.png",
]


@pytest.fixture(autouse=True)  # Automatically use in tests.
def mute_signals(request: Any) -> None:
    """Muting signals.

    see also: https://www.cameronmaske.com/muting-django-signals-with-a-pytest-fixture/
    """
    # Skip applying, if marked with `enabled_signals`
    if "enable_signals" in request.keywords:
        return

    signals = [
        post_save,
    ]
    restore = {}
    for signal in signals:
        # Temporally remove the signal's receivers (a.k.a attached functions)
        restore[signal] = signal.receivers
        signal.receivers = []

    def restore_signals() -> None:
        """When the test tears down, restore the signals."""
        for signal, receivers in restore.items():
            signal.receivers = receivers

    # Called after a test has finished.
    request.addfinalizer(restore_signals)


@pytest.fixture
def factory() -> APIRequestFactory:
    """Fixture for Returning APIRequestFactory."""
    return APIRequestFactory()


@pytest.fixture
def client() -> APIClient:
    """Fixture for Returning APIClient."""
    return APIClient()


@pytest.fixture
def sources() -> list[str]:
    """Return source path strings."""
    return SOURCE_PATHS


@pytest.fixture
def single_resource() -> Union[list[Model], Model]:
    """Return baked Resource models."""
    return baker.make("app.Resource", source=SOURCE_PATHS[0])


@pytest.fixture
def resources() -> list[Any]:
    """Return baked Resource models."""
    resources = []
    for url in SOURCE_PATHS:
        model = baker.make("app.Resource", source=url)
        resources.append(model)
    return resources
