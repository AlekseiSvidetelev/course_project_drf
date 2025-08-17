from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.com",
        )
        self.habit = Habit.objects.create(
            location="Парк",
            start_time="12:00",
            action="Пойти в парк",
            is_pleasant=False,
            periodicity=1,
            time_to_complete=99,
            is_public=True,
            user=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habit-detail", args=(self.habit.id,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(data.get("user"), self.user.id)
        self.assertEqual(data.get("location"), self.habit.location)
        self.assertEqual(data.get("start_time"), "12:00:00")
        self.assertEqual(data.get("action"), self.habit.action)
        self.assertEqual(data.get("is_pleasant"), False)
        self.assertEqual(data.get("periodicity"), 1)
        self.assertEqual(data.get("rewards"), None)
        self.assertEqual(data.get("time_to_complete"), self.habit.time_to_complete)
        self.assertEqual(
            data.get("is_public"),
            True,
        )

    def test_habit_create(self):
        url = reverse("habits:habit-list")
        data = {
            "location": "Дом",
            "start_time": "22:00:00",
            "action": "Читать книгу",
            "is_pleasant": False,
            "rewards": "Шоколадка",
            "periodicity": 1,
            "time_to_complete": 90,
            "is_public": False,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Habit.objects.all().count(),
            2,
        )

    def test_habit_update(self):
        url = reverse("habits:habit-detail", args=(self.habit.id,))
        data = {
            "location": "Дом",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(data.get("user"), self.user.id)
        self.assertEqual(data.get("location"), "Дом")
        self.assertEqual(data.get("start_time"), "12:00:00")
        self.assertEqual(data.get("action"), self.habit.action)
        self.assertEqual(data.get("is_pleasant"), False)
        self.assertEqual(data.get("periodicity"), 1)
        self.assertEqual(data.get("rewards"), None)
        self.assertEqual(data.get("time_to_complete"), self.habit.time_to_complete)
        self.assertEqual(
            data.get("is_public"),
            True,
        )

    def test_habit_delete(self):
        url = reverse("habits:habit-detail", args=(self.habit.id,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            Habit.objects.all().count(),
            0,
        )

    def test_habit_list(self):
        url = reverse("habits:habit-list")
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
                {
                    "id": self.habit.id,
                    "periodicity": self.habit.periodicity,
                    "time_to_complete": self.habit.time_to_complete,
                    "location": self.habit.location,
                    "start_time": "12:00:00",
                    "action": self.habit.action,
                    "is_pleasant": self.habit.is_pleasant,
                    "rewards": None,
                    "is_public": self.habit.is_public,
                    "user": self.user.id,
                    "related_habits": None,
                }
            ],
        }
        self.assertEqual(response.json(), result)
