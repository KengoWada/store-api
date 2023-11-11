from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users.views import urls

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    *urls,
]
