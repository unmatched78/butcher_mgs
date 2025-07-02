from rest_framework.routers import DefaultRouter
from .views import EmailTemplateViewSet

router = DefaultRouter()
router.register(r"templates", EmailTemplateViewSet, basename="email-templates")

urlpatterns = router.urls
