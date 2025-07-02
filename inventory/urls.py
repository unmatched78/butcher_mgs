from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ItemViewSet,
    StockEntryViewSet,
    StockExitViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet,   basename="categories")
router.register(r"items",      ItemViewSet,        basename="items")
router.register(r"entries",    StockEntryViewSet,  basename="entries")
router.register(r"exits",      StockExitViewSet,   basename="exits")

urlpatterns = router.urls
