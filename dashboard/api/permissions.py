from rest_framework import permissions 

class CustomPermissions(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        # Allow read-only access for all users.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow full access to admin users.
        if request.user.is_staff:
            return True
        
        # Allow editing and deletion operations of complaints to porters only
        if hasattr(obj, 'hostel') and hasattr(obj, 'student'):
            if request.user.is_student and obj.hostel == request.user.hostel:
                return True 
            return request.user.is_porter and obj.hostel == request.user.hostel
        
        if hasattr(obj, "user"):
            return obj.user == request.user
    
        
class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return request.user.is_staff 