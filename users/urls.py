from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users import views

urlpatterns = [
    path("register/", views.RegisterUserAPIView.as_view(), name="register-user"),
    path("login/", views.LoginUserAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("email/verify/", views.verify_email_address, name="verify-email-address"),
    path(
        "email/resend/",
        views.resend_email_verification_email,
        name="resend-email-verification-email",
    ),
]
