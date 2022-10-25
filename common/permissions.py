from rest_framework import permissions
from common.models import User



# class IsSuperAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_admin

# class IsOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.uid == obj.user_id
    
# class IsAdmin(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.role == 'admin'
   
# class IsEditor(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.role == 'editor'

# class IsWriter(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.role == 'writer'

# class IsPOST(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.method =='POST'
# class IsGET(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.method =='GET'
# class IsUPDATE(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.method =='PATCH' or request.method == 'PUT'
# class IsDELETE(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.method =='DELETE'
    
    
class DetailPermissons(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if(request.user.role=='admin'):
            return True
        # owner
        if(request.user.uid == obj.user_id):
            return True
        # not loggedin
        if(request.user.is_anonymous and request.method == 'GET'):
            return True
        # editor can do everything except delete. if is owner will do everything as per above conditions
        if(request.user.role == "editor" and request.method not in ['DELETE']):
            return True
        
        return False
    
class ListPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'reader' and request.method != "POST" 