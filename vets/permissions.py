from rest_framework.permissions import BasePermission

class IsVet(BasePermission):
    """
    Allows access only to users with role='vet'.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            getattr(request.user, "role", None) == "vet"
        )
