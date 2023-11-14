from http import HTTPStatus

from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler as default_exception_handler


def exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        response = {"error": "Authentication credentials were not provided."}
        return Response(response, status=HTTPStatus.UNAUTHORIZED)

    return default_exception_handler(exc, context)
