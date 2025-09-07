from django.db.models import Q
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginations import CustomPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description=(
            "Получение списка привычек с возможностью фильтрации и пагинации.\n\n"
            "**Доступные фильтры:**\n"
            "- `user` (int): Фильтр по ID пользователя\n"
            "- `is_public` (bool): Фильтр по публичности привычки\n\n"
            "**Примеры запросов:**\n"
            "- `GET /habits/?user=1` - привычки пользователя с ID=1\n"
            "- `GET /habits/?is_public=true` - все публичные привычки\n\n"
            "**Ответы:**\n"
            "- `HTTP 200 OK`: Успешный запрос, возвращает список привычек\n"
            "- `HTTP 401 Unauthorized`: Требуется аутентификация\n"
        ),
        manual_parameters=[
            openapi.Parameter(
                "user", openapi.IN_QUERY, description="Фильтр по ID пользователя", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                "is_public",
                openapi.IN_QUERY,
                description="Фильтр по публичности (true/false)",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={200: HabitSerializer(many=True), 401: "Требуется аутентификация"},
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description=(
            "Удаление привычки по идентификатору. "
            "Требует прав администратора или владельца привычки.\n\n"
            "**Параметры пути:**\n"
            "- `id` (int): Идентификатор привычки\n\n"
            "**Ответы:**\n"
            "- `HTTP 204 No Content`: Успешное удаление\n"
            "- `HTTP 404 Not Found`: Привычка не найдена\n"
            "- `HTTP 403 Forbidden`: Нет прав для удаления\n\n"
        ),
        responses={204: "Привычка успешно удалёна", 403: "Доступ запрещён", 404: "Привычка не найдена"},
    ),
)
class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    # сортировка и фильтрация
    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        "user",
        "is_public",
    )

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()
        if self.request.user.is_superuser:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(Q(user=self.request.user) | Q(is_public=True))

    def get_permissions(self):
        if self.action in ["update", "retrieve", "partial_update", "destroy"]:
            self.permission_classes = [IsOwner]
        elif self.action == ["list", "create"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
