from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication

from core.permissions import IsStaffOrReadOnly


class AuthenticatedAPIViewMixin(APIView):
    """APIView mixin with JWTAuthentication."""

    authentication_classes = [JWTAuthentication]


class StaffOrReadOnlyAPIViewMixin(AuthenticatedAPIViewMixin):
    """APIView mixin with permissions to allow only staff to create and update objects."""

    permission_classes = [IsStaffOrReadOnly]
