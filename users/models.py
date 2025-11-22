

from django.db import models
from django.contrib.auth.models import User
import uuid


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, default="Null")
    phone_number = models.CharField(max_length=20, default="Null")
    blood_group = models.CharField(max_length=3, default="Null")
    age = models.IntegerField(null=True, default="Null")
    address = models.CharField(max_length=255, default="Null")
    short_bio = models.TextField(max_length=300, default="Null")
    visible_to_doctors = models.BooleanField(default=True)

    def __str__(self):
        return self.user.email

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, default="Null")
    age = models.CharField(max_length=20, default="Null")
    address = models.CharField(max_length=200, default="Null")
    qualification = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255, default="Null")
    short_bio = models.TextField(max_length=300, default="Null")

    # New fields
    phone_number = models.CharField(max_length=20, default="Null" )
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
    
