"""momoichigo URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path

from .settings import DEBUG

urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/", include("momoichigo.app.urls")),
]

if DEBUG:
    urlpatterns.append(path("admin/", admin.site.urls))
