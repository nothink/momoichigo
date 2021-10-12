"""momoichigo URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from momoichigo.app import views
from momoichigo.settings import DEBUG

schema_view = get_schema_view(
    openapi.Info(
        title="momoichigo API",
        default_version="v0",
        description="ICHIGO KOHINATA",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gakongakon@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include("momoichigo.app.urls")),
    # auth
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/twitter/login/", views.TwitterLoginView.as_view(), name="twitter_login"),
    path(
        "auth/twitter/connect/",
        views.TwitterConnectView.as_view(),
        name="twitter_connect",
    ),
    # schema
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
]

if DEBUG:
    # admin
    urlpatterns.append(path("admin/", admin.site.urls))
    # schema
    urlpatterns.append(
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        )
    )
