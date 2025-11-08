from django.contrib import admin
from users.models import PatientProfile, DoctorProfile
# Register your models here.

admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
