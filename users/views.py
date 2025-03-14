from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .serializers import UserSerializer
from .permissions import IsSelfOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de usuarios.
    - Los usuarios pueden ver y modificar solo su propia cuenta.
    - Los administradores pueden gestionar todos los usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Asignar permisos:
        - Para crear (POST), no hay restricción.
        - Para las otras acciones (GET, PUT, PATCH, DELETE), solo el propio usuario o admin puede hacerlo.
        """
        if self.action == 'create':
            # Permitir acceso a cualquiera para crear un usuario
            permission_classes = [AllowAny]
        else:
            # Para otras acciones (ver, editar, eliminar) solo el usuario mismo o admin pueden acceder
            permission_classes = [IsSelfOrAdmin]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        - Si el usuario es administrador, obtiene todos los usuarios.
        - Si el usuario es normal, solo obtiene su propio perfil.
        """
        if self.request.user.is_staff:
            return super().get_queryset()
        return User.objects.filter(id=self.request.user.id)
