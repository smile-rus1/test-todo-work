from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from todo.models import User
from .serializers import UserRegistrationSerializer


@extend_schema(tags=["Registration"])
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
