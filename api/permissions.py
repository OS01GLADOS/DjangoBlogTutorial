from rest_framework import permissions

class AuthorAndStaffEdit(permissions.BasePermission):
    
    edit_methods = ('PUT', 'PATCH', 'DELETE', 'GET')

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if obj.author == request.user:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False