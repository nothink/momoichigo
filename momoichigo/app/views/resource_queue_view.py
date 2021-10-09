"""momoichigo views."""
from __future__ import annotations

import io
import logging
from typing import Any, List, Tuple
from urllib.parse import urlparse


import pendulum
import requests
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from slack_sdk.errors import SlackApiError
from slack_sdk.web.client import WebClient

from momoichigo import settings
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
        """Get serializers.

        Overwrites for using custom ListSerializers.
        sa: https://medium.com/swlh/f73da6af7ddc
        ** warning: this overwrite makes BrowsableAPI bad. **
        """
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

        collected, covered = self.__fetch_resources(sources)
        # 収集しきれなかった分は再度追加
        remains = list(set(sources) - set(collected) - set(covered))
        remain_modles = [models.ResourceQueue(source=r) for r in remains]
        models.ResourceQueue.objects.bulk_create(remain_modles)

        if len(collected) == 0:
            return Response(data=collected, status=status.HTTP_204_NO_CONTENT)

        self.__send_slack_message(self.__build_slack_msg(collected))

        return Response(data=collected, status=status.HTTP_201_CREATED)

    # ----------------- utility functions -----------------
    @staticmethod
    def __fetch_resources(urls: List[str]) -> Tuple[List[str], List[str]]:
        """Fetch and create Resource instance from source path.

        limit: 30 sec.
        """
        begin = pendulum.now()
        collected = []
        covered = []
        for url in urls:
            # Resource レコードを作成
            # その状態で get method で対象リソースをfetch
            instance = models.Resource()
            try:
                instance.source = url
                instance.validate_unique(exclude=["file"])
            except ValidationError:
                # ValidationErrorが出たなら既出なので無視対象
                covered.append(instance.source)
                continue

            res = requests.get(url)
            if res.status_code == 200 and len(res.content) > 0:
                path = urlparse(url).path[1:]

                # ファイル配置先はストレージのキー生成ルールに則る
                instance.file.save(path, io.BytesIO(res.content))
                logger.info("[fetch] " + instance.source)

                instance.full_clean(validate_unique=True)
                instance.save()

                collected.append(instance.source)
            # 合計時間が30秒を超えたら一旦キューの処理をやめる
            if pendulum.now().diff(begin).in_seconds() > 30:
                break
        # 収集結果と無視対象を返す
        return (collected, covered)

    @staticmethod
    def __send_slack_message(body: str) -> None:
        """Send messages to slack."""
        try:
            client = WebClient(token=settings.SLACK_API_TOKEN)
            client.chat_postMessage(text=body, channel="#resources")
        except SlackApiError as e:
            logger.error(e)

    @staticmethod
    def __build_slack_msg(sources: List[str]) -> str:
        """Create message strings for send to slack."""
        return ":strawberry: \n" + " \n".join(sources) + "\n :strawberry: "
