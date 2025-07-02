from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and 
            getattr(request.user, "role", None) == "client"
        )

class IsShopStaff(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and 
            getattr(request.user, "role", None) == "shop"
        )
