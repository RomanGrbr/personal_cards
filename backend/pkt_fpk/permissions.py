from rest_framework.permissions import BasePermission


class IsAuthorized(BasePermission):
    """Только авторизованному пользователю"""

    def has_permission(self, request, view):
        return bool(request.META.get('REMOTE_USER'))
