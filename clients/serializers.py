from rest_framework import serializers
from .models import Shop, CustomerProfile
from users.models import Customer  # original model for fields

class ShopSerializer(serializers.ModelSerializer):
    shop_id      = serializers.IntegerField(source="id", read_only=True)
    shop_name    = serializers.CharField(source="shop_name", read_only=True)
    shop_address = serializers.CharField(source="shop_address", read_only=True)
    shop_email   = serializers.CharField(source="shop_email", read_only=True)
    shop_phone   = serializers.CharField(source="shop_phone", read_only=True)

    class Meta:
        model = Shop
        fields = ["shop_id", "shop_name", "shop_address", "shop_email", "shop_phone"]


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        # Assuming Customer has only user FK and M2M; expose contact via User
        fields = ["id", "user", "created", "updated"]
        read_only_fields = ["id", "created", "updated"]
