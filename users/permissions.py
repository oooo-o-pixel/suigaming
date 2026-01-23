from rest_framework.permissions import BasePermission
from django.utils import timezone


# Access if user is a host, admin, or a player temporarily elevated to host role
class IsHostOrTempHost(BasePermission):
    def has_permission(self, request, _view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        # Admin and hosts always have access
        if user.role in ['host', 'admin']:
            return True
        
        # Check for temporary host status
        if user.role == 'player' and hasattr(user, 'temporary_host_until'):
            return (
                user.temporary_host_until is not None
                and user.temporary_host_until > timezone.now()
            )
        
        return False   # <-- explicit fallback


# Custom permission to only allow admins to access certain views
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


# Custom permission to allow host users to access their own resources
class IsHostUser(BasePermission):
    def has_object_permission(self, request, view, obj):   # <-- added obj
        return request.user.is_authenticated and request.user.role == 'host'
    

# Custom permission to allow players to access their own resources
class IsPlayerUser(BasePermission):
    def has_object_permission(self, request, view, obj):   # <-- added obj
        return request.user.is_authenticated and request.user.role == 'player'
