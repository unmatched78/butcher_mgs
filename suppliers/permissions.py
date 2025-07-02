from rest_framework.permissions import BasePermission

class IsShopStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "shop"

class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "supplier"
