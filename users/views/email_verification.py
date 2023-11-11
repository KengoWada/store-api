from http import HTTPStatus

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.utils import verify_token

from users.models import User
from users.utils import send_email_verification_email

__all__ = ("resend_email_verification_email", "verify_email_address")


@api_view(["POST"])
def resend_email_verification_email(request):
    """Resend email address verification email when user requests."""
    email = request.data.get("email")

    user = User.objects.filter(email=email).first()
    if user and not user.is_email_verified and user.is_active:
        subject = "Please Verify Your Email Address"
        send_email_verification_email(
            user.name,
            user.email,
            subject,
            "verify_email.html",
        )

    response = {"message": "An email has been sent."}
    return Response(response, status=HTTPStatus.OK)


@api_view(["PATCH"])
def verify_email_address(request):
    """Verify a users email address from token."""
    token = request.data.get("token")

    email = verify_token(token)
    if not email:
        response = {"error": "Invalid token."}
        return Response(response, status=HTTPStatus.BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if user and not user.is_email_verified and user.is_active:
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

    response = {"message": "Done"}
    return Response(response, status=HTTPStatus.OK)
