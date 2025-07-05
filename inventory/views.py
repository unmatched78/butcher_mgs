# inventory/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Item, StockEntry, StockExit
from .serializers import CategorySerializer, ItemSerializer, StockEntrySerializer, StockExitSerializer
from config.permissions import IsShopStaff
from suppliers.models import Quotation, SupplierProfile
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return Category.objects.filter(shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop_profile)

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return Item.objects.filter(shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop_profile)

class StockEntryViewSet(viewsets.ModelViewSet):
    serializer_class = StockEntrySerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return StockEntry.objects.filter(item__shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        serializer.save()

class StockExitViewSet(viewsets.ModelViewSet):
    serializer_class = StockExitSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return StockExit.objects.filter(item__shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        item = serializer.validated_data["item"]
        quantity = serializer.validated_data["quantity"]
        entries = StockEntry.objects.filter(item=item).aggregate(total=Sum("quantity"))["total"] or 0
        exits = StockExit.objects.filter(item=item).aggregate(total=Sum("quantity"))["total"] or 0
        available = entries - exits
        if quantity > available:
            raise serializers.ValidationError({"quantity": "Insufficient stock available."})
        serializer.save()

class InventoryListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get(self, request):
        items = Item.objects.filter(shop=request.user.shop_profile)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class InventoryReorderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def post(self, request):
        item_id = request.data.get("item_id")
        item = Item.objects.filter(id=item_id, shop=request.user.shop_profile).first()
        if not item:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        # Create a quotation for the shop's suppliers
        suppliers = SupplierProfile.objects.filter(shops=request.user.shop_profile)
        for supplier in suppliers:
            Quotation.objects.create(
                supplier=supplier,
                shop=request.user.shop_profile,
                item=item,
                proposed_price=item.unit_price,
                status="pending"
            )
        return Response({"detail": "Reorder request sent to suppliers"})

class InventoryMarkUsedView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def post(self, request):
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity", 1)
        item = Item.objects.filter(id=item_id, shop=request.user.shop_profile).first()
        if not item:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        entries = StockEntry.objects.filter(item=item).aggregate(total=Sum("quantity"))["total"] or 0
        exits = StockExit.objects.filter(item=item).aggregate(total=Sum("quantity"))["total"] or 0
        available = entries - exits
        if quantity > available:
            return Response({"detail": "Insufficient stock available"}, status=status.HTTP_400_BAD_REQUEST)
        StockExit.objects.create(
            item=item,
            quantity=quantity,
            sold_price=item.unit_price,
            sold_to="Internal use"
        )
        return Response({"detail": "Item marked as used"})

class InventoryTrendsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get(self, request):
        items = Item.objects.filter(shop=request.user.shop_profile)
        increasing = []
        decreasing = []
        one_month_ago = timezone.now() - timedelta(days=30)
        
        for item in items:
            recent_entries = StockEntry.objects.filter(
                item=item,
                received_at__gte=one_month_ago
            ).aggregate(total=Sum("quantity"))["total"] or 0
            recent_exits = StockExit.objects.filter(
                item=item,
                issued_at__gte=one_month_ago
            ).aggregate(total=Sum("quantity"))["total"] or 0
            if recent_entries > recent_exits:
                increasing.append(item.category.name)
            elif recent_exits > recent_entries:
                decreasing.append(item.category.name)
        
        return Response({
            "increasing": list(set(increasing)),
            "decreasing": list(set(decreasing))
        })