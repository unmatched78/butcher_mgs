from rest_framework import viewsets, permissions
from .models import Category, Item, StockEntry, StockExit
from .serializers import (
    CategorySerializer,
    ItemSerializer,
    StockEntrySerializer,
    StockExitSerializer,
)
from .permissions import IsShopStaff

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class    = CategorySerializer
    permission_classes  = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return Category.objects.filter(shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop_profile)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class    = ItemSerializer
    permission_classes  = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return Item.objects.filter(shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop_profile)


class StockEntryViewSet(viewsets.ModelViewSet):
    serializer_class    = StockEntrySerializer
    permission_classes  = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        # entries for items in this shop
        return StockEntry.objects.filter(item__shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        # no need to set shop—the item carries it
        serializer.save()


# inventory/views.py
class StockExitViewSet(viewsets.ModelViewSet):
    serializer_class = StockExitSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return StockExit.objects.filter(item__shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        item = serializer.validated_data["item"]
        quantity = serializer.validated_data["quantity"]
        # Calculate current stock
        entries = StockEntry.objects.filter(item=item).aggregate(total=models.Sum("quantity"))["total"] or 0
        exits = StockExit.objects.filter(item=item).aggregate(total=models.Sum("quantity"))["total"] or 0
        available = entries - exits
        if quantity > available:
            raise serializers.ValidationError({"quantity": "Insufficient stock available."})
        serializer.save()
