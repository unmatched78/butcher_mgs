# communications/serializers.py
from rest_framework import serializers
from .models import EmailTemplate, CommunicationHistory

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ["id", "name", "subject", "content", "type", "last_used"]

class CommunicationHistorySerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source="template.name", read_only=True)

    class Meta:
        model = CommunicationHistory
        fields = ["id", "template_name", "subject", "recipient_email", "sent_date", "status", "type"]