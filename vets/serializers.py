from rest_framework import serializers
from inventory.models import Cow
from .models import CowInspection, SlaughterApproval

class CowInspectionSerializer(serializers.ModelSerializer):
    cow_id = serializers.PrimaryKeyRelatedField(
        queryset=Cow.objects.all(),
        source="cow",
        write_only=True
    )

    class Meta:
        model = CowInspection
        fields = [
            "id", "cow_id", "vet", "inspection_type",
            "notes", "is_fit_for_consumption", "date"
        ]
        read_only_fields = ["id", "vet", "date"]

    def create(self, validated_data):
        validated_data["vet"] = self.context["request"].user
        return super().create(validated_data)


class SlaughterApprovalSerializer(serializers.ModelSerializer):
    cow_id = serializers.PrimaryKeyRelatedField(
        queryset=Cow.objects.all(),
        source="cow",
        write_only=True
    )

    class Meta:
        model = SlaughterApproval
        fields = [
            "id", "cow_id", "vet", "is_approved",
            "comments", "approved_at"
        ]
        read_only_fields = ["id", "vet", "approved_at"]

    def create(self, validated_data):
        validated_data["vet"] = self.context["request"].user
        return super().create(validated_data)
