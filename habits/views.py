from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.paginations import CustomPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()

    def get_queryset(self):
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
