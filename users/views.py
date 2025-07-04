# users/core/views.py
import logging
from rest_framework import viewsets, status, generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes, api_view, permission_classes
from django.contrib.auth import get_user_model
from .models import *
from rest_framework import filters
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from decimal import Decimal
from django.db import transaction 
from config.permissions import *
User = get_user_model()
# Module‐level logger
logger = logging.getLogger(__name__)  # best practice for namespaced logging

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the base class to get the original tokens
        data = super().validate(attrs)
        # Attach your user info
        data['user'] = {
            'id':       self.user.id,
            'username': self.user.username,
            'email':    self.user.email,
            'role':     self.user.role, 
            # add more fields as needed
        }
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # --- Inject these claims into BOTH access & refresh tokens ---
        token['user_id']     = user.id
        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsShopStaff])
def register_supplier(request):
    serializer = SupplierRegistrationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()
        supplier_profile = user.supplier_profile
        # Return the supplier profile data
        return Response(
            SupplierProfileSerializer(supplier_profile).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsShopStaff])
def register_customer(request):
    serializer = CustomerRegistrationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()
        customer_profile = user.client_profile
        # Return the customer profile data
        return Response(
            CustomerProfileSerializer(customer_profile).data,
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)