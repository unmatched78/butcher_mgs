from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SupplierProfileViewSet,
    SupplierInvitationViewSet,
    QuotationViewSet,
    SupplyEntryViewSet,
)

router = DefaultRouter()
router.register(r"profile",      SupplierProfileViewSet,    basename="supplier-profile")
router.register(r"invitations",  SupplierInvitationViewSet, basename="supplier-invitations")
router.register(r"quotations",   QuotationViewSet,          basename="quotations")
router.register(r"deliveries",   SupplyEntryViewSet,        basename="deliveries")

urlpatterns = [
    path("", include(router.urls)),
]
