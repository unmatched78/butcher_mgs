from rest_framework import serializers
from .models import Category, Item, StockEntry, StockExit

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "sku", "name", "category", "unit_price"]
        read_only_fields = ["id"]

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
