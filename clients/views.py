from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Shop, CustomerProfile
from .serializers import ShopSerializer, CustomerProfileSerializer
from config.permissions import *
from inventory.models import Item
from inventory.serializers import ItemSerializer

class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public endpoints for clients:
      - list all shops
      - retrieve a single shop
    """
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["get"], url_path="items")
    def items(self, request, pk=None):
        """
        GET /api/clients/shops/{pk}/items/
        List items for this shop.
        """
        shop = self.get_object()
        items = Item.objects.filter(shop=shop)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class CustomerProfileViewSet(viewsets.GenericViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin):
    """
    Authenticated clients can GET and PUT their own profile.
    """
    serializer_class   = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsClient]

    def get_object(self):
        return CustomerProfile.objects.get(user=self.request.user)
