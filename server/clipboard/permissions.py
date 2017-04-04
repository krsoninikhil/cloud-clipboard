from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permissions to only allow owner of an object to edit it.
    """

    # This file is taken from djandorestframework tutorial
    def has_object_permission(self, request, view, obj):
        # anyone can read i.e. GET, OPTIONS, etc
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user
