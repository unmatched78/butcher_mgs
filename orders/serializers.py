from rest_framework import serializers
from .models import Order, OrderLine

class OrderLineSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=None,  # set in __init__
        source="item",
        write_only=True
    )
    class Meta:
        model = OrderLine
        fields = ["id", "item_id", "quantity", "unit_price", "line_total"]
        read_only_fields = ["id", "unit_price", "line_total"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # bind item queryset to the shop's items
        shop = self.context.get("shop")
        if shop:
            self.fields["item_id"].queryset = shop.items.all()
        else:
            from inventory.models import Item
            self.fields["item_id"].queryset = Item.objects.none()

# orders/serializers.py
class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(source="customer", write_only=True, queryset=Customer.objects.all())
    shop = serializers.PrimaryKeyRelatedField(queryset=ShopProfile.objects.all())

    class Meta:
        model = Order
        fields = ["id", "shop", "customer_id", "status", "total", "created_at", "updated_at", "lines"]
        read_only_fields = ["id", "status", "total", "created_at", "updated_at"]

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
            # Check stock
            entries = StockEntry.objects.filter(item=item).aggregate(total=models.Sum("quantity"))["total"] or 0
            exits = StockExit.objects.filter(item=item).aggregate(total=models.Sum("quantity"))["total"] or 0
            available = entries - exits
            if quantity > available:
                raise serializers.ValidationError({f"lines[{lines_data.index(line)}].quantity": "Insufficient stock."})
            line["order"] = order
            ol = OrderLine.objects.create(**line)
            total += ol.line_total
        order.total = total
        order.save()
        return order