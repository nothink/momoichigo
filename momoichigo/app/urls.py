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
    # schema
    path("schema", get_schema_view()),
    # auth
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/twitter/login/", views.TwitterLoginView.as_view(), name="twitter_login"),
    path(
        "auth/twitter/connect/",
        views.TwitterConnectView.as_view(),
        name="twitter_connect",
    ),
]
