from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    SupplierProfile,
    SupplierInvitation,
    Quotation,
    SupplyEntry,
)
from .serializers import (
    SupplierProfileSerializer,
    SupplierInvitationSerializer,
    QuotationSerializer,
    SupplyEntrySerializer,
)
from config.permissions import *

class SupplierProfileViewSet(viewsets.GenericViewSet,
                             viewsets.mixins.RetrieveModelMixin,
                             viewsets.mixins.UpdateModelMixin):
    """
    supplier users can GET/PUT their own profile.
    """
    serializer_class    = SupplierProfileSerializer
    permission_classes  = [permissions.IsAuthenticated, IsSupplier]

    def get_object(self):
        return SupplierProfile.objects.get(user=self.request.user)


class SupplierInvitationViewSet(viewsets.ModelViewSet):
    """
    Shop staff:
      - list/create invitations
      - approve/reject supplier responses via custom actions
    """
    queryset           = SupplierInvitation.objects.all()
    serializer_class   = SupplierInvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsShopStaff]

    def get_queryset(self):
        # only invitations for this shop
        return self.queryset.filter(shop=self.request.user.shop_profile)

    @action(detail=True, methods=["post"], url_path="respond")
    def respond(self, request, pk=None):
        """
        Supplier uses this (via token) to accept/reject invite:
        POST /api/suppliers/invitations/{id}/respond/ { "accept": true }
        """
        invite = self.get_object()
        accept = request.data.get("accept", False)
        if accept:
            invite.status       = "accepted"
            invite.responded_at = timezone.now()
            # link the supplier user automatically (if exists)
            try:
                supplier_user = settings.AUTH_USER_MODEL.objects.get(email=invite.email)
                profile = supplier_user.supplier_profile
                profile.shops.add(invite.shop)
            except Exception:
                pass
        else:
            invite.status       = "rejected"
            invite.responded_at = timezone.now()
        invite.save()
        return Response({"status": invite.status})


class QuotationViewSet(viewsets.ModelViewSet):
    """
    - Supplier: create/list their own quotations
    - Shop staff: list/approve/reject quotations for their shop via custom action
    """
    serializer_class    = QuotationSerializer
    permission_classes  = [permissions.IsAuthenticated]
    queryset            = Quotation.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == "supplier":
            return self.queryset.filter(supplier=user.supplier_profile)
        return self.queryset.filter(shop=user.shop_profile)

    def get_permissions(self):
        if self.action in ["create",]:
            return [permissions.IsAuthenticated(), IsSupplier()]
        if self.action in ["approve", "reject"]:
            return [permissions.IsAuthenticated(), IsShopStaff()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        quote = self.get_object()
        quote.status      = "approved"
        quote.responded_at= timezone.now()
        quote.save()
        return Response({"status":"approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        quote = self.get_object()
        quote.status      = "rejected"
        quote.responded_at= timezone.now()
        quote.notes       = request.data.get("notes", "")
        quote.save()
        return Response({"status":"rejected"})


class SupplyEntryViewSet(viewsets.ModelViewSet):
    """
    - Supplier: record deliveries against their approved quotations
    - Shop staff: list/update (accept/reject) deliveries
    """
    serializer_class    = SupplyEntrySerializer
    permission_classes  = [permissions.IsAuthenticated]
    queryset            = SupplyEntry.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == "supplier":
            return self.queryset.filter(quotation__supplier=user.supplier_profile)
        return self.queryset.filter(quotation__shop=user.shop_profile)

    def get_permissions(self):
        if self.action in ["create",]:
            return [permissions.IsAuthenticated(), IsSupplier()]
        if self.action in ["update","partial_update"]:
            return [permissions.IsAuthenticated(), IsShopStaff()]
        return [permissions.IsAuthenticated()]
