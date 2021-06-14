from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserAPIView, login_user

urlpatterns = [
    path('user/', UserAPIView.as_view()),
    path('login/', login_user),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
