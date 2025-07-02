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

class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        source="customer",
        queryset=None,  # set in __init__
        write_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id", "shop", "customer_id", "status", "total",
            "created_at", "updated_at", "lines"
        ]
        read_only_fields = ["id", "shop", "status", "total", "created_at", "updated_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # shop from context
        shop = self.context.get("shop")
        if shop:
            self.fields["shop"].default = shop
            self.fields["customer_id"].queryset = shop.created_customers.all()
        else:
            from users.models import Customer
            self.fields["customer_id"].queryset = Customer.objects.none()

    def create(self, validated_data):
        lines_data = validated_data.pop("lines")
        order = Order.objects.create(**validated_data)
        total = 0
        for line in lines_data:
            line["order"] = order
            ol = OrderLine.objects.create(**line)
            total += ol.line_total
        order.total = total
        order.save()
        return order
