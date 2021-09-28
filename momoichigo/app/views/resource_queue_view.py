"""momoichigo views."""
from __future__ import annotations

import io
import logging
from collections.abc import Iterable
from typing import Any

import pendulum
import requests
from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from slack_sdk.errors import SlackApiError
from slack_sdk.web.client import WebClient

from momoichigo import settings
from momoichigo.app import models, serializers

logger = logging.getLogger(__name__)


class ResourceQueueViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """API endpoints for resource_queues.

    Allow: List(Get)
    """

    queryset = models.ResourceQueue.objects.all().order_by("resource")
    serializer_class = serializers.ResourceQueueSerializer

    def list(
        self: ResourceQueueViewSet, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """Overwrite to 'list' method."""
        begin = pendulum.now()
        all_queues = models.ResourceQueue.objects.all().order_by("created")
        if len(all_queues) == 0:
            # 基本的にここに落ちるはず
            return Response(status=status.HTTP_204_NO_CONTENT)

        collected: list[str] = []
        for queue in all_queues:
            # get method で対象リソースをfetchして格納
            res = requests.get(queue.resource.source)
            if res.status_code == 200 and len(res.content) > 0:
                queue.resource.file.save(queue.resource.key, io.BytesIO(res.content))
                logger.info("[fetch] " + queue.resource.source)
                collected.append(queue.resource.source)
                queue.delete()
            # 合計時間が20秒を超えたら一旦キューの処理をやめる
            if pendulum.now().diff(begin).in_seconds() > 20:
                break

        # slack メッセージを送信
        try:
            client = WebClient(token=settings.SLACK_API_TOKEN)
            client.chat_postMessage(
                text=self.__build_slack_msg(collected), channel="#resources"
            )
        except SlackApiError as e:
            logger.error(e)

        # 開発環境のみ、最後に取りこぼしのResourceをさらっておく
        if settings.DEBUG:
            self.__collect_empty()

        return Response(status=status.HTTP_202_ACCEPTED)

    @staticmethod
    def __collect_empty() -> None:
        """Collect empty resources into queue."""
        empties = models.Resource.objects.filter(file="")
        for instance in empties:
            exists = models.ResourceQueue.objects.filter(resource=instance)
            if len(exists) == 0:
                models.ResourceQueue.objects.create(resource=instance)

    @staticmethod
    def __build_slack_msg(sources: Iterable[str]) -> str:
        """Create message strings for send to slack."""
        return ":strawberry: \n" + " \n".join(sources) + "\n :strawberry: "
