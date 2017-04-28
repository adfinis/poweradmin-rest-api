from rest_framework import permissions
from sydns.api.models import User


class IsRecordOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        owner = User.objects.get(username__iexact=request.user.username)
        return obj.domain.zones.filter(owner=owner.id).exists()
