from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow staff members to create and update objects."""

    message = {"error": "Permission denied"}

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            return False

        if request.method == "DELETE":
            return False

        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            return False

        if request.method == "DELETE":
            return False

        return request.user.is_authenticated and request.user.is_staff
