"""Urls."""
from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from momoichigo.app import views

router = routers.DefaultRouter()
router.register(r"resources", views.ResourceViewSet)
router.register(r"girls", views.GirlViewSet)
router.register(r"scenes", views.SceneViewSet)


urlpatterns = [
    path("", include(router.urls)),
    # sa: https://djoser.readthedocs.io/en/latest/index.html
    path("schema", get_schema_view()),
]
