"""views."""
from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError
from django.http import QueryDict
from rest_framework import mixins, request, response, status, viewsets

from momoichigo.app.models import Resource
from momoichigo.app.serializers import ResourceSerializer


class ResourceViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """api endpoints for resource.

    Allow: Create(POST), List(Get), Retrieve(Get)
    """

    queryset = Resource.objects.all().order_by("source")
    serializer_class = ResourceSerializer

    def create(self: ResourceViewSet, request: request.Request) -> response.Response:
        """Overwrite to 'create' method."""
        if isinstance(request.data, list):
            is_created = False
            # 1件でも被るとコケて仕様を満たさないので、many=Trueは使えない
            for item in request.data:
                try:
                    self.__create_one(item)
                    is_created = True
                except ValidationError:
                    pass
            if is_created:
                return response.Response(status=status.HTTP_201_CREATED)
            else:
                # 1件も作成されなかったら HTTP 204: No Content.
                return response.Response(status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                self.__create_one(request.data)
                return response.Response(status=status.HTTP_201_CREATED)
            except ValidationError:
                return response.Response(status=status.HTTP_204_NO_CONTENT)

    def __create_one(self: ResourceViewSet, data: QueryDict | Any) -> None:
        """Create a model once."""
        serializer = self.get_serializer(data=data, many=False)
        # create if valid
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
        else:
            raise ValidationError("Duplicated source.")
