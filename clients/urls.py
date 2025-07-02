from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShopViewSet, CustomerProfileViewSet

router = DefaultRouter()
router.register(r"shops", ShopViewSet, basename="shops")
router.register(r"profile", CustomerProfileViewSet, basename="customer-profile")

urlpatterns = [
    path("", include(router.urls)),
]
