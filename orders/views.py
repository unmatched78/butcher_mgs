from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsClient, IsShopStaff

# orders/views.py
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related("shop", "customer").prefetch_related("lines")

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsClient()]
        if self.action in ("update", "partial_update"):
            return [permissions.IsAuthenticated(), IsShopStaff()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            return self.queryset.filter(customer=user.client_profile)
        return self.queryset.filter(shop=user.shop_profile)

    def get_serializer_context(self):
        return super().get_serializer_context()  # Remove shop defaulting