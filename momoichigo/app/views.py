"""views."""
from __future__ import annotations

from typing import Any

from django.http import QueryDict
from rest_framework import request, response, status, viewsets

from momoichigo.app.models import Resource
from momoichigo.app.serializers import ResourceSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    """api endpoints for resource."""

    queryset = Resource.objects.all().order_by("source")
    serializer_class = ResourceSerializer

    def create(self: ResourceViewSet, request: request.Request) -> response.Response:
        """Overwrite create method."""

        def _create_once(data: QueryDict | Any) -> None:
            """Create once."""
            serializer = self.get_serializer(data=data, many=False)
            # create if valid
            if serializer.is_valid(raise_exception=False):
                self.perform_create(serializer)

        if isinstance(request.data, list):
            # 1件でも被るとコケて仕様を満たさないので、many=Trueは使えない
            for item in request.data:
                s = self.get_serializer(data=item, many=False)
                _create_once(s)
        else:
            s = self.get_serializer(data=request.data, many=False)
            _create_once(s)
        return response.Response(status=status.HTTP_201_CREATED)
