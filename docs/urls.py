from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentTemplateViewSet, DocumentInstanceViewSet

router = DefaultRouter()
router.register(r"templates", DocumentTemplateViewSet, basename="doc-templates")
router.register(r"instances", DocumentInstanceViewSet, basename="doc-instances")

urlpatterns = [
    path("", include(router.urls)),
]
