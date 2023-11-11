from os import environ

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

ADMIN_URL = "admin/"
ENV = environ.get("DJANGO_ENV") or "DEV"

if ENV == "PROD":
    admin.site.site_header = settings.ADMIN_SITE_HEADER
    admin.site.site_title = settings.ADMIN_SITE_TITLE
    admin.site.index_title = settings.ADMIN_INDEX_TITLE
    ADMIN_URL = settings.ADMIN_URL


urlpatterns = [
    path("auth/", include("users.urls", namespace="auth")),
    # path('products/', include('products.urls')),
]

if ENV != "TESTING":
    urlpatterns.append(path(f"{ADMIN_URL}", admin.site.urls))
