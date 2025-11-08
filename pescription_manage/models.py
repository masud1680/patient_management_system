# core/models.py
from django.db import models
from users.models import PatientProfile, DoctorProfile

def prescription_upload_path(instance, filename):
    return f"prescriptions/{instance.patient.user.id}/{filename}"



class Prescription(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="prescriptions")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="prescriptions")
    diagnosis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=prescription_upload_path, null=True, blank=True)

    def __str__(self):
        return f"Prescription #{self.id} - {self.patient.user.email}"

class PrescriptionMedicine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="medicines", blank=True)
    medicine_name = models.CharField(max_length=255, blank=True)
    dosage = models.CharField(max_length=100, help_text="e.g., 500 mg or 5 ml", blank=True)
    times_per_day = models.PositiveSmallIntegerField(help_text="How many times per day", default=1, blank=True)
    duration_days = models.PositiveIntegerField(help_text="For how many days", default=1, blank=True)
    instruction = models.CharField(max_length=255, blank=True, help_text="e.g., After meal or Before bed")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.medicine_name} ({self.dosage})"
