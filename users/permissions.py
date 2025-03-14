from rest_framework import permissions


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permite a los usuarios gestionar solo su propia cuenta,
    excepto los administradores, que pueden gestionar a todos.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_staff
