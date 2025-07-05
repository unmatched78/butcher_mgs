# users/core/views.py
import logging
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from django.contrib.auth import get_user_model
from .models import *
from rest_framework import filters
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import MyTokenRefreshSerializer
from decimal import Decimal
from django.db import transaction 
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
from inventory.models import Item as InventoryItem
from rest_framework import generics
from config.permissions import *
from suppliers.models import SupplierProfile
from suppliers.serializers import SupplierProfileSerializer
from users.serializers import SupplierRegistrationSerializer, CustomerRegistrationSerializer
from clients.serializers import CustomerProfileSerializer
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


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
# users/views.py
class ShopTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != "shop":
            return Response({"detail": "Unauthorized"}, status=403)
        tasks = [
            {"id": 1, "title": "Approve delivery for Order #1234", "priority": "high"},
            {"id": 2, "title": "Review expiring inventory items", "priority": "medium"}
            # Add logic to fetch from models, e.g., Task.objects.filter(shop=user.shop_profile)
        ]
        return Response(tasks)


class ShopMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != "shop":
            return Response({"detail": "Unauthorized"}, status=403)
        total_sales = Order.objects.filter(shop=user.shop_profile).aggregate(total=Sum("total"))["total"] or 0
        pending_orders = Order.objects.filter(shop=user.shop_profile, status="pending").count()
        low_stock_items = InventoryItem.objects.filter(shop=user.shop_profile, quantity__lte=10).count()
        expiring_items = InventoryItem.objects.filter(shop=user.shop_profile, expiry_date__lte=timezone.now() + timedelta(days=3)).count()
        return Response({
            "totalSales": f"RWF {total_sales}",
            "pendingOrders": str(pending_orders),
            "lowStockItems": str(low_stock_items),
            "expiringItems": str(expiring_items),
        })

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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsShopStaff])
def customer_list(request):
    customers = Customer.objects.filter(client_for_shops=request.user.shop_profile)
    serializer = CustomerProfileSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)