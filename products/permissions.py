from rest_framework import permissions, status


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff members to certain actions
    """

    message = {'message': 'Permission denied',
               'status': status.HTTP_403_FORBIDDEN}

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            return False

        return request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            return False

        return request.user.is_authenticated and request.user.is_staff
