from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class HasPermission(BasePermission):
    def __init__(self, permission):
        self.permission = permission

    def has_permission(self, request, view):
        if not request.user.has_perm(self.permission):
            raise PermissionDenied("Недостаточно прав.")
        return True


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_employee:
            raise PermissionDenied("Недостаточно прав.")
        return True
