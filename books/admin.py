from django.contrib import admin
from .models import Book, Page


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    search_fields = ['title', 'author__username']
    list_filter = ['created_at', 'updated_at', 'author']
    ordering = ['created_at']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['book', 'number', 'content']
    search_fields = ['book__title', 'content']
    list_filter = ['book']
    ordering = ['book', 'number']
