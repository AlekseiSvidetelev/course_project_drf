from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.paginations import CustomPagination
from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import PublicUserSerializer, UserSerializer


@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description=(
            "Удаление пользователя по идентификатору. "
            "Требует прав администратора или пользователя.\n\n"
            "**Параметры пути:**\n"
            "- `id` (int): Идентификатор пользователя\n\n"
            "**Ответы:**\n"
            "- `HTTP 204 No Content`: Успешное удаление\n"
            "- `HTTP 404 Not Found`: Пользователь не найден\n"
            "- `HTTP 403 Forbidden`: Нет прав для удаления\n\n"
        ),
        responses={204: "Пользователь успешно удалён", 403: "Доступ запрещён", 404: "Пользователь не найден"},
    ),
)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            requested_user_id = self.kwargs.get("pk")
            current_user_id = self.request.user.id
            if str(current_user_id) == str(requested_user_id):
                return UserSerializer
        elif self.action == "create":
            return UserSerializer
        return PublicUserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "list":
            self.permission_classes = [
                IsAuthenticated,
            ]
        elif self.action == "create":
            self.permission_classes = [
                AllowAny,
            ]
        elif self.action == "retrieve":
            self.permission_classes = [
                IsAuthenticated,
            ]
        elif self.action == "update" or self.action == "partial_update":
            self.permission_classes = [
                IsOwnerOrAdmin,
            ]
        elif self.action == "destroy":
            self.permission_classes = [
                IsOwnerOrAdmin,
            ]
        return super().get_permissions()
