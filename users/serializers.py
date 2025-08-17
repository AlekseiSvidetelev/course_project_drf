from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habit
from users.models import User


class UserSerializer(ModelSerializer):
    habits = serializers.SerializerMethodField()

    def get_habits(self, obj):
        """Получаем список привычек текущего пользователя."""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            habits = Habit.objects.filter(user=request.user).count()
            return habits
        return []

    class Meta:
        model = User
        fields = [
            "id",
            "date_joined",
            "first_name",
            "last_name",
            "email",
            "phone",
            "tg_name",
            "avatar",
            "habits",
        ]


class PublicUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "avatar")
