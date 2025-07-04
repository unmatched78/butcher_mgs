from rest_framework import viewsets, permissions
from .models import DocumentTemplate, DocumentInstance
from .serializers import DocumentTemplateSerializer, DocumentInstanceSerializer
from config.permissions import *

class DocumentTemplateViewSet(viewsets.ModelViewSet):
    """
    Shop staff can CRUD their own document templates.
    """
    serializer_class   = DocumentTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        return DocumentTemplate.objects.filter(shop=self.request.user.shop_profile)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user.shop_profile)


class DocumentInstanceViewSet(viewsets.ModelViewSet):
    """
    Shop staff and vets can create/fill and list/retrieve instances.
    """
    serializer_class   = DocumentInstanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopOrVet]

    def get_queryset(self):
        user = self.request.user
        qs = DocumentInstance.objects.select_related("template", "created_by")
        if user.role == "shop":
            # shop staff see instances for their shop's templates
            return qs.filter(template__shop=user.shop_profile)
        # vets see all instances (or you can limit to templates of certain shops)
        return qs

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
