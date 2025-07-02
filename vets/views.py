from rest_framework import viewsets, permissions, mixins
from .models import CowInspection, SlaughterApproval
from .serializers import CowInspectionSerializer, SlaughterApprovalSerializer
from .permissions import IsVet

class CowInspectionViewSet(viewsets.ModelViewSet):
    """
    - Vets (role='vet') can create/update/delete their inspections.
    - Shop staff can list & retrieve inspections for their own cows.
    """
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
        # adjust this filter to match how you link cows to shops:
        return qs.filter(cow__client=user.shop_profile)


class SlaughterApprovalViewSet(viewsets.GenericViewSet,
                               mixins.CreateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               mixins.UpdateModelMixin):
    """
    - Vets can create or update the sole approval per cow.
    - Shop staff can list & retrieve approvals for their cows.
    """
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
        return qs.filter(cow__client=user.shop_profile)
