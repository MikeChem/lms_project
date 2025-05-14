from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """
    Разрешение: пользователь принадлежит к группе 'Модератор'
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модератор').exists()


class IsOwner(permissions.BasePermission):
    """
    Разрешение: пользователь является владельцем объекта
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOrModeratorReadOnly(permissions.BasePermission):
    """
    Разрешение: модератор может читать и редактировать,
    владелец может делать всё.
    """
    def has_object_permission(self, request, view, obj):
        # Все могут читать (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == request.user or request.user.groups.filter(name='Модератор').exists()

        # Редактирование доступно модератору
        if request.method in ['PUT', 'PATCH']:
            return obj.owner == request.user or request.user.groups.filter(name='Модератор').exists()

        # Удаление и создание — только владельцу
        return obj.owner == request.user