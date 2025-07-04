from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/vets/", include("vets.urls")),
    path("api/suppliers/", include("suppliers.urls")),
    path("api/clients/", include("clients.urls")),
    path("api/inventory/", include("inventory.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/docs/", include("docs.urls")),

]
