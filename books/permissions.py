from rest_framework import permissions


class IsAuthorOrEditor(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un editor o el autor del libro.
    """

    def has_permission(self, request, view):
        # Comprobaciones de permisos globales (en toda la vista)
        if request.user.role == 'editor':
            return True  # Los editores pueden hacer cualquier acción
        if request.user.role == 'reader' and view.action in ['list', 'retrieve']:
            return True  # Los lectores solo pueden listar y ver libros
        return False

    def has_object_permission(self, request, view, obj):
        # Comprobaciones de permisos a nivel de objeto (sobre un libro específico)
        if request.user.role == 'editor':
            # Los editores pueden actualizar y eliminar libros que hayan creado
            if view.action in ['update', 'partial_update', 'destroy']:
                return obj.author == request.user  # Solo el autor puede actualizar o eliminar su libro
            return True  # Los editores pueden ver todos los libros

        if request.user.role == 'reader' and view.action in ['list', 'retrieve']:
            return True  # Los lectores solo pueden ver libros (listar y recuperar)

        return False
