import json

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model


class UserAPITests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="testuser@example.com",
            password="testpassword",
            role="reader"
        )

        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')
        self.url = reverse('user-list')

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword'
        }
        json_data = json.dumps(data)

        response = self.client.post(reverse('user-list'), json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_user_login(self):
        data = {
            'username': 'testuser@example.com',
            'password': 'testpassword'
        }
        json_data = json.dumps(data)

        response = self.client.post(self.login_url, json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_refresh_token(self):
        refresh_token = str(RefreshToken.for_user(self.user))
        data = {
            'refresh': refresh_token
        }
        response = self.client.post(self.refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_unauthenticated_user_cannot_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_user_list(self):
        token = str(RefreshToken.for_user(self.user).access_token)
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
