from rest_framework.permissions import BasePermission
from . models import CustomUser


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == CustomUser.TEACHER

  
class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == CustomUser.STUDENT
