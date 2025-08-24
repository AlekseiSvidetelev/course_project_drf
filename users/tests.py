from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com",
        )
        self.client.force_authenticate(user=self.user)

    def test_user_retrieve(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("email"),
            self.user.email,
        )

    def test_users_create(self):
        url = reverse("users:user-list")
        data = {"email": "test8@example.com", "password": "12345678"}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            User.objects.all().count(),
            2,
        )

    def test_users_update(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {
            "first_name": "Test Name Update",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("first_name"),
            "Test Name Update",
        )

    def test_user_delete(self):
        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            User.objects.all().count(),
            0,
        )

    def test_user_list(self):
        url = reverse("users:user-list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {"id": self.user.pk, "first_name": None, "last_name": None, "email": self.user.email, "avatar": None}
            ],
        }
        self.assertEqual(response.json(), result)
