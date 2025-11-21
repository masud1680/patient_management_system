# from rest_framework.permissions import BasePermission

# class IsDoctor(BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated 
#             and request.user.groups.filter(name="doctor").exists()
#         )

# class IsPatient(BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated 
#             and request.user.groups.filter(name="patient").exists()
#         )
