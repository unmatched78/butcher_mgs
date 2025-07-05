from rest_framework import viewsets, permissions
from .models import EmailTemplate
from .serializers import EmailTemplateSerializer
from config.permissions import *

class EmailTemplateViewSet(viewsets.ModelViewSet):
    """
    Shop staff can list & edit their shop’s email templates.
    """
    serializer_class   = EmailTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return EmailTemplate.objects.filter(shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        # On first save of a new code, associate it with the shop
        serializer.save(shop=self.request.user.shop_profile)
