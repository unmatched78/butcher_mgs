from rest_framework.permissions import BasePermission

class IsShopStaff(BasePermission):
    """Allows access only to users with role='shop'."""
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "shop"
        )

class IsShopOrVet(BasePermission):
    """Allows access to shop‑staff or vets."""
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
            and getattr(request.user, "role", None) in ("shop", "vet")
        )
