# core/permissions.py
from rest_framework import permissions
from .models import DoctorProfile, PatientProfile

# class IsDoctor(permissions.BasePermission):
#     def has_permission(self, request, view):

from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'doctor'

# class IsPatient(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return hasattr(request.user, 'patientprofile')


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups == 'patient'

class IsDoctorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(request.user, 'doctorprofile')
