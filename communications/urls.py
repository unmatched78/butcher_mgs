# communications/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailTemplateViewSet, CommunicationHistoryViewSet, SendCommunicationView

router = DefaultRouter()
router.register(r"templates", EmailTemplateViewSet, basename="templates")
router.register(r"history", CommunicationHistoryViewSet, basename="history")

urlpatterns = [
    path("", include(router.urls)),
    path("send/", SendCommunicationView.as_view(), name="send-communication"),
]