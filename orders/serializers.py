# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderLine
from inventory.models import Item
from users.models import Customer, ShopProfile
from django.db.models import Sum

class OrderLineSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.none(),
        source="item",
        write_only=True
    )
    name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        model = OrderLine
        fields = ["id", "item_id", "name", "quantity", "unit_price", "line_total"]
        read_only_fields = ["id", "unit_price", "line_total", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shop = self.context.get("shop")
        if shop:
            self.fields["item_id"].queryset = shop.items.all()

class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        source="customer",
        write_only=True,
        queryset=Customer.objects.all()
    )
    shop = serializers.PrimaryKeyRelatedField(queryset=ShopProfile.objects.all())
    customer = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "shop", "customer_id", "customer", "status", "total", "date", "lines"]
        read_only_fields = ["id", "status", "total", "date", "customer"]

    def get_customer(self, obj):
        return {
            "name": obj.customer.user.get_full_name() or obj.customer.user.username,
            "email": obj.customer.user.email,
            "phone": obj.customer.client_for_shops.first().shop_phone  # Assuming phone from shop
        }

    def validate(self, attrs):
        shop = attrs["shop"]
        customer = attrs["customer"]
        if shop not in customer.client_for_shops.all():
            raise serializers.ValidationError({"shop": "Customer is not linked to this shop."})
        return attrs

    def create(self, validated_data):
        lines_data = validated_data.pop("lines")
        order = Order.objects.create(**validated_data)
        total = 0
        for line in lines_data:
            item = line["item"]
            quantity = line["quantity"]
            entries = StockEntry.objects.filter(item=item).aggregate(total=Sum("quantity"))["total"] or 0
            exits = StockExit.objects.filter(item=item).aggregate(total=Sum("quantity"))["total"] or 0
            available = entries - exits
            if quantity > available:
                raise serializers.ValidationError({f"lines[{lines_data.index(line)}].quantity": "Insufficient stock."})
            line["order"] = order
            ol = OrderLine.objects.create(**line)
            total += ol.line_total
        order.total = total
        order.save()
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance