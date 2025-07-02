from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CowInspectionViewSet, SlaughterApprovalViewSet

router = DefaultRouter()
router.register(r"inspections", CowInspectionViewSet, basename="inspections")
router.register(r"approvals",   SlaughterApprovalViewSet, basename="slaughter-approvals")

urlpatterns = [
    path("", include(router.urls)),
]
