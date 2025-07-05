from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="user-register"),
    path('auth/token/',  MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("auth/refresh/", MyTokenRefreshView.as_view(),     name="token_refresh"),
    #path("auth/refresh/", TokenRefreshView.as_view(),    name="token_refresh"),
    path('register-supplier/', register_supplier, name='register-supplier'),
    path('register-customer/', register_customer, name='register-customer'),
    path("customers/", customer_list, name="customer-list"),  # New endpoint
    path('shop/metrics/', ShopMetricsView.as_view(), name='shop-metrics'),
    path('shop/tasks/', ShopTasksView.as_view(), name='shop-tasks'),
]
