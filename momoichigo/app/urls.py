"""Urls."""
from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from momoichigo.app import views

router = routers.DefaultRouter()
router.register(
    r"resource-queues", views.ResourceQueueViewSet, basename="resource-queue"
)
router.register(r"resources", views.ResourceViewSet, basename="resource")


urlpatterns = [
    path("", include(router.urls)),
    path("schema", get_schema_view()),
]
