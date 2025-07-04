from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ShopProfile, VetProfile

User = get_user_model()
# users/serializers.py
class RegistrationSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(write_only=True, required=False)
    shop_email = serializers.EmailField(write_only=True, required=False)
    shop_phone = serializers.CharField(write_only=True, required=False)
    shop_address = serializers.CharField(write_only=True, required=False)
    license_number = serializers.CharField(write_only=True, required=False)
    vet_email = serializers.EmailField(write_only=True, required=False)
    vet_phone = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username", "email", "password", "role",
            "shop_name", "shop_email", "shop_phone", "shop_address",
            "license_number", "vet_email", "vet_phone",
        ]

    def validate(self, attrs):
        role = attrs.get("role")
        if role == "shop":
            for f in ("shop_name", "shop_email", "shop_phone"):
                if not attrs.get(f):
                    raise serializers.ValidationError({f: "Required for shop users."})
        elif role == "vet":
            for f in ("license_number", "vet_email", "vet_phone"):
                if not attrs.get(f):
                    raise serializers.ValidationError({f: "Required for vet users."})
        elif role not in ("client", "supplier"):
            raise serializers.ValidationError({"role": "Invalid role."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        shop_data = {k: validated_data.pop(k) for k in ("shop_name", "shop_email", "shop_phone", "shop_address") if k in validated_data}
        vet_data = {k: validated_data.pop(k) for k in ("license_number", "vet_email", "vet_phone") if k in validated_data}
        user = User.objects.create(role=role, **validated_data)
        user.set_password(password)
        user.save()
        if role == "shop":
            ShopProfile.objects.create(user=user, **shop_data)
        elif role == "vet":
            VetProfile.objects.create(user=user, **vet_data)
        elif role == "client":
            Customer.objects.create(user=user)
        elif role == "supplier":
            SupplierProfile.objects.create(user=user)
        return user