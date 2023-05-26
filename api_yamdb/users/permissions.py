from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == User.RoleChoice.ADMIN
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.role == User.RoleChoice.ADMIN
            or request.user.is_superuser
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.role == User.RoleChoice.ADMIN
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (
                request.user.role == User.RoleChoice.ADMIN
                or request.user.is_superuser
            )
        )


'''
class IsUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.RoleChoice.USER
        )

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.RoleChoice.MODERATOR
        )
'''


class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user == obj.author
            or request.user.role == User.RoleChoice.MODERATOR
            or request.user.role == User.RoleChoice.ADMIN
            or request.user.is_superuser
        )
