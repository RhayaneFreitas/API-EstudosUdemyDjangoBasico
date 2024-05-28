# Basepermissions -> Permissiões Personalizadas esobrescreve seus métodos, como has_permission e has_object_permission.
# from rest_framework.permissions import BasePermission
from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission): # Poderia ser só BasePermissions
    """Allow user to edit their own profile"""
    
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id