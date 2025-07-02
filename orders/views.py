from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .permissions import IsClient, IsShopStaff

class OrderViewSet(viewsets.ModelViewSet):
    """
    - Clients (role='client') can create & list their own orders.
    - Shop staff (role='shop') can list & update status of orders for their shop.
    """
    serializer_class   = OrderSerializer
    queryset           = Order.objects.select_related("shop", "customer").prefetch_related("lines")

    def get_permissions(self):
        if self.action in ("create",):
            return [permissions.IsAuthenticated(), IsClient()]
        if self.action in ("update", "partial_update"):
            return [permissions.IsAuthenticated(), IsShopStaff()]
        # list & retrieve: both roles
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            return self.queryset.filter(customer=user.client_profile)
        return self.queryset.filter(shop=user.shop_profile)

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        # always include shop in context
        if self.request.user.role == "shop":
            ctx["shop"] = self.request.user.shop_profile
        elif self.request.user.role == "client":
            ctx["shop"] = self.request.user.client_profile.client_for_shops.first()
        return ctx

    def perform_update(self, serializer):
        # allow shop to change status
        serializer.save()
