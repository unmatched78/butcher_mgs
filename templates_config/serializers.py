from rest_framework import serializers
from .models import EmailTemplate

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ["id", "code", "subject", "body", "updated_at"]
        read_only_fields = ["id", "updated_at"]
