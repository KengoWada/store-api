from http import HTTPStatus

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.utils import generate_token, verify_token

from users.models import User
from users.serializers import UserSerializer
from users.utils import send_forgot_password_email

__all__ = ("reset_password", "forgot_password")


@api_view(["PATCH"])
def reset_password(request):
    """Change a users password."""
    token = request.data.get("token")
    email = verify_token(token)
    if not email:
        response = {"error": "Invalid token"}
        return Response(response, status=HTTPStatus.BAD_REQUEST)

    user = User.objects.filter(email=email).first()
    if user and user.is_active and user.password_reset_token == token:
        serializer = UserSerializer(
            user, data={"password": request.data.get("password")}, partial=True
        )
        if not serializer.is_valid():
            response = {"error": serializer.errors}
            return Response(response, status=HTTPStatus.BAD_REQUEST)
        serializer.save()

    response = {"message": "Done"}
    return Response(response, status=HTTPStatus.OK)


@api_view(["POST"])
def forgot_password(request):
    """Send email with token to reset users password."""
    email = request.data.get("email")

    user = User.objects.filter(email=email).first()
    if user and user.is_active:
        token = generate_token(user.email)
        user.password_reset_token = token
        user.save(update_fields=["password_reset_token"])

        send_forgot_password_email(user.name, user.email, token)

    response = {"message": "Done"}
    return Response(response, status=HTTPStatus.OK)
