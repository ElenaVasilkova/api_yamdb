from rest_framework import viewsets
from .models import User
from .serializers import UserRegisterSerializer


class RegisterUserView(viewsets.CreateAPIView):
    pass


class APIGetToken:
    pass