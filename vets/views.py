from rest_framework import viewsets, permissions, mixins
from .models import CowInspection, SlaughterApproval
from .serializers import CowInspectionSerializer, SlaughterApprovalSerializer
from .permissions import IsVet

# vets/views.py
class CowInspectionViewSet(viewsets.ModelViewSet):
    serializer_class = CowInspectionSerializer
    queryset = CowInspection.objects.select_related("cow", "vet")

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsVet()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "vet":
            return qs.filter(vet=user)
        return qs.filter(cow__shop=user.shop_profile)

class SlaughterApprovalViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = SlaughterApprovalSerializer
    queryset = SlaughterApproval.objects.select_related("cow", "vet")

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update"):
            return [permissions.IsAuthenticated(), IsVet()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == "vet":
            return qs.filter(vet=user)
        return qs.filter(cow__shop=user.shop_profile)