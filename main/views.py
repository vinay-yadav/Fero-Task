from rest_framework import generics, permissions
from .serializers import UserRegisterSerializer
from .models import User


class RegisterUserAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
