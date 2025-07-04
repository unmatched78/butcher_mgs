from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ShopProfile, VetProfile
from suppliers.models import SupplierProfile
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


class SupplierRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField()
    contact_email = serializers.EmailField()
    contact_phone = serializers.CharField()
    address = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'company_name', 'contact_email', 'contact_phone', 'address']

    def create(self, validated_data):
        # Create a new user with role 'supplier'
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='supplier'
        )
        # Create the supplier profile
        supplier_profile = SupplierProfile.objects.create(
            user=user,
            company_name=validated_data['company_name'],
            contact_email=validated_data['contact_email'],
            contact_phone=validated_data['contact_phone'],
            address=validated_data.get('address', '')
        )
        # Link the supplier to the shop owner's shop
        shop = self.context['request'].user.shop_profile
        supplier_profile.shops.add(shop)
        return user

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # Create a new user with role 'client'
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='client',
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        # Create the customer profile
        customer_profile = Customer.objects.create(user=user)
        # Link the customer to the shop owner's shop
        shop = self.context['request'].user.shop_profile
        customer_profile.client_for_shops.add(shop)
        return user