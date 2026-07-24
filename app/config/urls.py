from django.contrib import admin
from django.urls import include, path

from config.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("auth/", include("social_django.urls", namespace="social")),
    path("users/", include("apps.users.urls")),
]
