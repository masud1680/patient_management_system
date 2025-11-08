# core/permissions.py
from rest_framework import permissions
from .models import DoctorProfile, PatientProfile

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'doctorprofile')

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'patientprofile')

class IsDoctorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(request.user, 'doctorprofile')
