from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Category.objects.filter(user=self.request.user).prefetch_related('tasks')
        return Category.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Tasks"])
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
