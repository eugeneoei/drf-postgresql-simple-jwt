from rest_framework.permissions import BasePermission

class IsUserObjectOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user