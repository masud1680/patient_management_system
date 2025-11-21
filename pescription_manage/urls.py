# core/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import  PrescriptionCountSingle, UniqueDoctorsForPatient, UniqueDoctorDetailsForPatient, PatientProfileViewSet, DoctorProfileViewSet, PrescriptionViewSet

router = routers.DefaultRouter()
router.register(r'patients', PatientProfileViewSet, basename='patient')
router.register(r'doctors', DoctorProfileViewSet, basename='doctor')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    path('', include(router.urls)),
    path("prescription-count/", PrescriptionCountSingle.as_view()),
    path("analytics/unique-doctors/", UniqueDoctorsForPatient.as_view()),
    path("analytics/unique-doctors/details/", UniqueDoctorDetailsForPatient.as_view()),
]
