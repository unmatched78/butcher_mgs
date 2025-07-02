from rest_framework import serializers
from .models import (
    SupplierProfile,
    SupplierInvitation,
    Quotation,
    SupplyEntry,
)
from users.models import ShopProfile
from django.utils import timezone

class SupplierProfileSerializer(serializers.ModelSerializer):
    shop_ids = serializers.PrimaryKeyRelatedField(
        source="shops", many=True, read_only=True
    )
    class Meta:
        model = SupplierProfile
        fields = ["id", "company_name", "contact_email", "contact_phone", "address", "shop_ids"]
        read_only_fields = ["id", "shop_ids"]


class SupplierInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierInvitation
        fields = ["id", "shop", "email", "token", "status", "created", "responded_at"]
        read_only_fields = ["id", "token", "status", "created", "responded_at"]

    def create(self, validated_data):
        invite = super().create(validated_data)
        # TODO: send email to invite.email with a link containing invite.token
        return invite


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ["id", "supplier", "shop", "item", "proposed_price", "status", "notes", "created", "responded_at"]
        read_only_fields = ["id", "status", "created", "responded_at", "shop", "supplier"]

    def create(self, validated_data):
        # supplier posts quote: set supplier and shop automatically
        user = self.context["request"].user
        supplier = user.supplier_profile
        shop     = validated_data["shop"]
        validated_data["supplier"] = supplier
        quotation = super().create(validated_data)
        return quotation


class SupplyEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyEntry
        fields = ["id", "quotation", "quantity", "delivered_at", "shop_accepted", "shop_notes"]
        read_only_fields = ["id", "delivered_at", "shop_accepted"]

    def update(self, instance, validated_data):
        # shop accepts/rejects delivery
        instance.shop_accepted = validated_data.get("shop_accepted", instance.shop_accepted)
        instance.shop_notes    = validated_data.get("shop_notes", instance.shop_notes)
        instance.save()
        return instance
