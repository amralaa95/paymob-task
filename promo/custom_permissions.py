from rest_framework import permissions
from profiles.models import User


class IsCanAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user and request.user.is_authenticated and request.user.role == User.ADMIN


class CanUsePromo(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role != User.ADMIN
