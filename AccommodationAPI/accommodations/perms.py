from rest_framework import permissions
from accommodations.models import UserEnum
class OwnerPerms(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user and request.user == obj.user
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == UserEnum.ADMIN.value

class IsInnkeeper(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == UserEnum.INKEEPER.value
    
class IsTenant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_role == UserEnum.TENANT.value