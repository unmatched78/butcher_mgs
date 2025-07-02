from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    """
    Grants access only to authenticated users with role='client'.
    """
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == "client"
        )
