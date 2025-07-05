# communications/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EmailTemplate, CommunicationHistory
from .serializers import EmailTemplateSerializer, CommunicationHistorySerializer
from config.permissions import IsShopStaff  # Adjust import for your permission class
from .utils import send_email
from django.utils import timezone

class EmailTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = EmailTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]  # Adjust permissions

    def get_queryset(self):
        return EmailTemplate.objects.filter(shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        serializer.save(last_used=timezone.now(), shop=self.request.user.shop_profile)
    def perform_update(self, serializer):
        serializer.save(last_used=timezone.now(), shop=self.request.user.shop_profile)

class CommunicationHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommunicationHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]  # Adjust permissions

    def get_queryset(self):
        return CommunicationHistory.objects.filter(shop=self.request.user.shop_profile)

class SendCommunicationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]  # Adjust permissions

    def post(self, request):
        shop = request.user.shop_profile
        if not shop:
            return Response({"detail": "Shop profile not found"}, status=status.HTTP_404_NOT_FOUND)
        shop_email= shop.email or  ""
        data = request.data
        subject = data.get("subject")
        content = data.get("content")
        recipient_email = data.get("recipient_email")
        template_id = data.get("template_id")
        communication_type = data.get("type", "custom")

        if not all([subject, content, recipient_email]):
            return Response({"detail": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            send_email(recipient_email,shop_email, subject, content)
            CommunicationHistory.objects.create(
                shop=shop,
                template_id=template_id,
                subject=subject,
                recipient_email=recipient_email,
                status="sent",
                type=communication_type,
            )
            if template_id:
                EmailTemplate.objects.filter(id=template_id).update(last_used=timezone.now())
            return Response({"detail": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            CommunicationHistory.objects.create(
                shop=shop,
                template_id=template_id,
                subject=subject,
                recipient_email=recipient_email,
                status="failed",
                type=communication_type,
                error_message=str(e),
            )
            return Response({"detail": "Failed to send email", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)