from rest_framework.permissions import BasePermission

class IsShopStaff(BasePermission):
    """
    Allows access only to authenticated users with role='shop'.
    """
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == "shop"
        )
