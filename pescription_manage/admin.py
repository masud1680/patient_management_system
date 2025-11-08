from django.contrib import admin
from pescription_manage.models import Prescription, PrescriptionMedicine
# Register your models here.

admin.site.register(Prescription)
admin.site.register(PrescriptionMedicine)