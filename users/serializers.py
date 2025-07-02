from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ShopProfile, VetProfile

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    # Additional fields for both roles:
    shop_name   = serializers.CharField(write_only=True, required=False)
    shop_email  = serializers.EmailField(write_only=True, required=False)
    shop_phone  = serializers.CharField(write_only=True, required=False)
    shop_address= serializers.CharField(write_only=True, required=False)
    license_number = serializers.CharField(write_only=True, required=False)
    vet_email      = serializers.EmailField(write_only=True, required=False)
    vet_phone      = serializers.CharField(write_only=True, required=False)
    password       = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = [
            "username", "email", "password", "role",
            # shop fields
            "shop_name", "shop_email", "shop_phone", "shop_address",
            # vet fields
            "license_number", "vet_email", "vet_phone",
        ]

    def validate(self, attrs):
        role = attrs.get("role")
        # For shop users, require shop_name etc.
        if role == "shop":
            for f in ("shop_name","shop_email","shop_phone"):
                if not attrs.get(f):
                    raise serializers.ValidationError({f: "This field is required for shop users."})
        # For vets, require license and contact
        elif role == "vet":
            for f in ("license_number","vet_email","vet_phone"):
                if not attrs.get(f):
                    raise serializers.ValidationError({f: "This field is required for vet users."})
        else:
            raise serializers.ValidationError({"role":"Invalid role."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        # Pop off profile data
        shop_data = { k: validated_data.pop(k) for k in ("shop_name","shop_email","shop_phone","shop_address") if k in validated_data }
        vet_data  = { k: validated_data.pop(k) for k in ("license_number","vet_email","vet_phone") if k in validated_data }

        # Create the user
        user = User.objects.create(role=role, **validated_data)
        user.set_password(password)
        user.save()

        # Create the appropriate profile
        if role == "shop":
            ShopProfile.objects.create(user=user, **shop_data)
        else:  # role == "vet"
            VetProfile.objects.create(user=user, **vet_data)

        return user
