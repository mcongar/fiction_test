from rest_framework import serializers
from .models import Book, Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'number', 'content']


class BookSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'created_at', 'updated_at', 'pages']
        read_only_fields = ['created_at', 'updated_at', 'author']

    def create(self, validated_data):
        pages_data = validated_data.pop('pages', [])
        book = Book.objects.create(author=self.context['request'].user, **validated_data)

        # Crear las páginas asociadas al libro (Bulk Create)
        pages_to_create = [
            Page(book=book, **page_data) for page_data in pages_data
        ]
        Page.objects.bulk_create(pages_to_create)  # Operación en lote (Reducimos las llamadas a la Base de Datos)

        return book

    def update(self, instance, validated_data):
        """Actualizar un libro y sus páginas."""
        pages_data = validated_data.pop('pages', None)
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        if pages_data is not None:
            # Usamos un conjunto para almacenar los números de página en la nueva lista de páginas
            new_page_numbers = {page_data['number'] for page_data in pages_data}

            # Eliminamos las páginas que no están en la nueva lista de páginas
            instance.pages.exclude(number__in=new_page_numbers).delete()

            # Actualizamos o creamos las páginas nuevas
            pages_to_create = []
            pages_to_update = []

            for page_data in pages_data:
                page_number = page_data['number']
                page = instance.pages.filter(number=page_number).first()

                if page:  # Si la página ya existe, la actualizamos
                    page.content = page_data.get('content', page.content)
                    pages_to_update.append(page)
                else:  # Si la página no existe, la creamos
                    pages_to_create.append(Page(book=instance, **page_data))

            # Bulk create para las nuevas páginas
            if pages_to_create:
                Page.objects.bulk_create(pages_to_create)

            # Bulk update para las páginas que se deben actualizar
            if pages_to_update:
                Page.objects.bulk_update(pages_to_update, ['content'])

        return instance
