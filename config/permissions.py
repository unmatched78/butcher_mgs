# permissions.py
# config/permissions.py
from rest_framework.permissions import BasePermission

class IsShopStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, "role", None) == "shop"
        )

class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, "role", None) == "supplier"
        )

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, "role", None) == "client"
        )

class IsVet(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, "role", None) == "vet"
        )