from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="user-register"),
    path("api/auth/token/",   TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(),    name="token_refresh"),
    path('register-supplier/', register_supplier, name='register-supplier'),
    path('register-customer/', register_customer, name='register-customer'),
]
