# users/views.py
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import *

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
