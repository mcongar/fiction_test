from django.db import models

from users.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE, limit_choices_to={'role': 'editor'})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.author.role != 'editor':
            raise ValueError("Only editors can be authors of books.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Page(models.Model):
    book = models.ForeignKey(Book, related_name="pages", on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    content = models.TextField()

    class Meta:
        unique_together = ('book', 'number')  # Asegura que no haya dos páginas con el mismo número en un libro
        ordering = ['number']

    def __str__(self):
        return f"Page {self.number} of {self.book.title}"
