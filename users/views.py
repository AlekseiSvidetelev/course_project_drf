from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import UserSerializer, PublicUserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
