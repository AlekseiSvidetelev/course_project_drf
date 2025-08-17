from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяем, является ли пользователь владельцем объекта"""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False


class IsOwnerOrAdmin(permissions.BasePermission):
    """Проверяем, является ли пользователь владельцем объекта или админом"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_superuser
