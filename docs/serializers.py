from rest_framework import serializers
from .models import DocumentTemplate, DocumentInstance

class DocumentTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTemplate
        fields = [
            "id", "name", "description",
            "schema", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

class DocumentInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentInstance
        fields = [
            "id", "template", "data",
            "created_by", "created_at"
        ]
        read_only_fields = ["id", "created_by", "created_at"]
