from email import message
from math import perm
from rest_framework import permissions
from common.models import User


class POSTPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        method =request.method
        
        if(method == "GET"):
            return True
        
        if(request.user.is_anonymous is False):
            role = request.user.role
            if(method in ["POST"] and role in ["admin",'editor','writer']):
                return True
        
        return False
class ObjectPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        method =request.method
        
        
        if(method == "GET"):
            return True
        
        if(request.user.is_anonymous is False):

            owner= obj.user_id.uid == request.user.uid
            role = request.user.role
            if(owner):
                return True

            if(method in ["PUT",'PATCH','DELETE'] and role in ['admin']):
                return True
        
            if(method in ["PUT",'PATCH'] and role in ['editor']):
                return True
        
        return False
    

class POSTCategoryPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        
        
        method =request.method
        if(method == "GET"):
            return True
        if(request.user.is_anonymous is False):
            role = request.user.role
            if(method in ["POST"] and role in ["admin"]):
                return True
        
        return False

class ObjectCategoryPermissions(permissions.BasePermission):
    print('df')
    def has_object_permission(self, request, view, obj):
        method =request.method
        if(method == "GET"):
            return True
        if(request.user.is_anonymous is False):
            print('ds')
            role = request.user.role
            print('iii')
            if(method in ["PUT",'PATCH','DELETE'] and role in ['admin']):
                return True
        
        return False



class POSTCommentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        method =request.method
        
        if(method == "GET"):
            return True
        
        if(request.user.is_anonymous is False):
            return True
        
        return False

class ObjectCommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        method =request.method

        if(method == "GET"):
            return True
        if(request.user.is_anonymous is False):
            owner= obj.user_id.uid == request.user.uid
            role = request.user.role
            if(method in ['DELETE'] and role in ['admin'] or owner):
                return True
        
        return False
