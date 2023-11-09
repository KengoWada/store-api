from http import HTTPStatus

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from users.utils import send_email_verification_email

__all__ = ("RegisterUserAPIView", "LoginUserAPIView")


class RegisterUserAPIView(APIView):
    email_subject = "Welcome to Online Store API"
    email_template = "welcome.html"

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            response = {"error": serializer.errors}
            return Response(response, status=HTTPStatus.BAD_REQUEST)

        serializer.save()
        user = serializer.data
        send_email_verification_email(
            user["name"], user["email"], self.email_subject, self.email_template
        )

        response = {"message": "Done"}
        return Response(response, status=HTTPStatus.CREATED)


class LoginUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            response = {"error": "Invalid credentials"}
            return Response(response, status=HTTPStatus.BAD_REQUEST)

        tokens = user.get_auth_tokens()
        serializer = UserSerializer(user)
        response = {"message": "Done", "user": serializer.data, **tokens}
        return Response(response, status=HTTPStatus.OK)
