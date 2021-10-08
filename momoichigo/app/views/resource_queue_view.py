"""momoichigo views."""
from __future__ import annotations

import io
import logging
from typing import Any

import pendulum
import requests
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from momoichigo.app import models, serializers

logger = logging.getLogger(__name__)


class ResourceQueueViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """Request Queue Views."""

    queryset = models.ResourceQueue.objects.all()
    serializer_class = serializers.ResourceQueueSerializer

    def get_serializer(
        self: ResourceQueueViewSet, *args: Any, **kwargs: Any
    ) -> Serializer:
        """Get serializers."""
        kwargs["context"] = self.get_serializer_context()
        if "data" in kwargs and isinstance(kwargs["data"], list):
            kwargs["many"] = True
            data = []
            for item in kwargs["data"]:
                if isinstance(item, str):
                    data.append({"source": item})
                else:
                    data.append(item)
            kwargs["data"] = data

        return self.get_serializer_class()(*args, **kwargs)

    def list(
        self: ResourceQueueViewSet, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """List method's overwrite."""
        with transaction.atomic():
            sources = [q.source for q in self.queryset]
            # 重複除去
            sources = list(set(sources))
            # クリーンアップ
            self.queryset.delete()
        # 要素なしならおしまい
        if len(sources) == 0:
            return Response(data=sources, status=status.HTTP_204_NO_CONTENT)

        begin = pendulum.now()
        collected = []
        for url in sources:
            # Resource レコードを作成
            # その状態で get method で対象リソースをfetch
            instance = models.Resource()
            try:
                instance.source = url
                instance.validate_unique(exclude=["file"])
            except ValidationError:
                continue

            res = requests.get(url)
            if res.status_code == 200 and len(res.content) > 0:

                # ファイル配置先はストレージのキー生成ルールに則る
                instance.file.save(instance.key, io.BytesIO(res.content))
                logger.info("[fetch] " + instance.source)

                instance.full_clean(validate_unique=True)
                instance.save()

                collected.append(instance.source)
            # 合計時間が30秒を超えたら一旦キューの処理をやめる
            if pendulum.now().diff(begin).in_seconds() > 30:
                break

        if len(collected) == 0:
            return Response(data=collected, status=status.HTTP_204_NO_CONTENT)

        return Response(data=collected, status=status.HTTP_201_CREATED)
