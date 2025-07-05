# inventory/serializers.py
from rest_framework import serializers
from .models import Category, Item, StockEntry, StockExit
from django.db.models import Sum

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]

class ItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    quantity = serializers.SerializerMethodField()
    stock_level = serializers.SerializerMethodField()
    unit = serializers.CharField(default="kg")  # Default unit, adjust as needed
    expiry_date = serializers.DateField(format="%Y-%m-%d", allow_null=True)
    last_updated = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ["id", "sku", "name", "category", "quantity", "unit", "expiry_date", "stock_level", "unit_price", "last_updated"]
        read_only_fields = ["id", "quantity", "stock_level", "last_updated"]

    def get_quantity(self, obj):
        entries = StockEntry.objects.filter(item=obj).aggregate(total=Sum("quantity"))["total"] or 0
        exits = StockExit.objects.filter(item=obj).aggregate(total=Sum("quantity"))["total"] or 0
        return entries - exits

    def get_stock_level(self, obj):
        quantity = self.get_quantity(obj)
        if quantity <= 10:
            return "Low"
        elif quantity <= 50:
            return "Medium"
        return "High"

    def get_last_updated(self, obj):
        latest_entry = StockEntry.objects.filter(item=obj).order_by("-received_at").first()
        latest_exit = StockExit.objects.filter(item=obj).order_by("-issued_at").first()
        entry_date = latest_entry.received_at if latest_entry else None
        exit_date = latest_exit.issued_at if latest_exit else None
        if entry_date and exit_date:
            return max(entry_date, exit_date).strftime("%Y-%m-%d")
        return (entry_date or exit_date or obj.item_ptr.created_at).strftime("%Y-%m-%d")

class StockEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockEntry
        fields = ["id", "item", "supplier", "quantity", "batch_no", "received_at"]
        read_only_fields = ["id", "received_at"]

class StockExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockExit
        fields = ["id", "item", "quantity", "sold_price", "sold_to", "issued_at"]
        read_only_fields = ["id", "issued_at"]