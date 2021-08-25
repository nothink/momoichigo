"""momoichigo views."""
from __future__ import annotations

from typing import Any

from django.http import QueryDict
from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from momoichigo.app import models, serializers


class ResourceViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """api endpoints for resource.

    Allow: Create(POST), List(Get), Retrieve(Get)
    """

    queryset = models.Resource.objects.all().order_by("source")
    serializer_class = serializers.ResourceSerializer

    def create(
        self: ResourceViewSet, request: Request, *args: Any, **kwargs: Any
    ) -> Response:
        """Overwrite to 'create' method."""
        response_list = []
        if isinstance(request.data, list):
            # multi records
            request_list = request.data
        else:
            # single record
            request_list = [request.data]
        # 1件でも被るとコケて仕様を満たさないので、many=Trueは使えない
        for item in request_list:
            result = self.__create_one(item)
            if result:
                response_list.append(result)
        if len(response_list) > 0:
            return Response(data=response_list, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def __create_one(self: ResourceViewSet, data: QueryDict | Any) -> str | None:
        """Create a model once."""
        serializer = self.get_serializer(data=data, many=False)
        # create if valid
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            return data["source"]
        return None
