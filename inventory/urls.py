# inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ItemViewSet,
    StockEntryViewSet,
    StockExitViewSet,
    InventoryListView,
    InventoryReorderView,
    InventoryMarkUsedView,
    InventoryTrendsView,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"items", ItemViewSet, basename="items")
router.register(r"entries", StockEntryViewSet, basename="entries")
router.register(r"exits", StockExitViewSet, basename="exits")

urlpatterns = [
    path("", include(router.urls)),
    path("inventory/", InventoryListView.as_view(), name="inventory-list"),
    path("inventory/reorder/", InventoryReorderView.as_view(), name="inventory-reorder"),
    path("inventory/mark-used/", InventoryMarkUsedView.as_view(), name="inventory-mark-used"),
    path("inventory/trends/", InventoryTrendsView.as_view(), name="inventory-trends"),
]