import json

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from books.models import Book


class BookAPITests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            email="test@example.com",
            password="testpassword",
            role="editor"
        )

        self.token = str(RefreshToken.for_user(self.user).access_token)

        self.book = Book.objects.create(
            title="Test Book",
            author=self.user,
        )

        self.url = reverse("book-list")

    def test_create_book(self):
        data = {
            "title": "New Book",
            "pages": [
                {"number": 1, "content": "Content of page 1"},
                {"number": 2, "content": "Content of page 2"}
            ]
        }
        json_data = json.dumps(data)

        response = self.client.post(self.url, json_data, content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_list_books(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "pages": [
                {"number": 1, "content": "Updated content of page 1"},
                {"number": 2, "content": "Updated content of page 2"}
            ]
        }
        json_data = json.dumps(data)
        response = self.client.put(reverse("book-detail", args=[self.book.id]), json_data,
                                   content_type='application/json', HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(reverse("book-detail", args=[self.book.id]),
                                      HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
