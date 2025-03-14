from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from .permissions import IsAuthorOrEditor
from rest_framework.permissions import IsAuthenticated


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrEditor]
