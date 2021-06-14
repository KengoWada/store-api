from rest_framework import permissions, status


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Custom permission class to allow users to only register if they aren't logged in
    """

    message = {'message': 'Permission denied',
               'status': status.HTTP_403_FORBIDDEN}

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        if request.user.is_anonymous:
            return False

        return request.user.is_authenticated
