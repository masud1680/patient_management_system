

from django.db import models
from django.contrib.auth.models import User
import uuid


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    visible_to_doctors = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255, blank=True)

    # New fields
    phone_number = models.CharField(max_length=20, blank=True)
    available_days = models.CharField(max_length=100, default="Mon-Fri Default")
    available_time = models.CharField(max_length=50, default="9 AM-5 PM Default")

    def __str__(self):
        return "Dr. " + self.user.last_name

    
class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
    
