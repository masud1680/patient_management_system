# core/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  Prescription, PrescriptionMedicine
# from users.serializers import DoctorProfileSerializer, PatientProfileSerializer
from users.models import PatientProfile, DoctorProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all(), write_only=True)

    class Meta:
        model = PatientProfile
        fields = ['id','user','user_id','phone_number','gender','blood_group', 'age','address','short_bio','visible_to_doctors']
        # read_only_fields = ['user']
        
class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all(), write_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['id','user','user_id','qualification','specialization','phone_number','gender','age','address','short_bio',]

class PrescriptionMedicineSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # allow update with id

    class Meta:
        model = PrescriptionMedicine
        fields = ['id','medicine_name','dosage','times_per_day','duration_days','instruction']

class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = PrescriptionMedicineSerializer(many=True)
    doctor = DoctorProfileSerializer(read_only=True)
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=DoctorProfile.objects.all(), write_only=True, required=False, allow_null=True)
    patient = PatientProfileSerializer(read_only=True)
    patient_id = serializers.PrimaryKeyRelatedField(source='patient', queryset=PatientProfile.objects.all(), write_only=True)

    class Meta:
        model = Prescription
        fields = ['id','doctor','doctor_id','patient','patient_id','diagnosis','image','medicines','created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        medicines_data = validated_data.pop('medicines', [])
        prescription = Prescription.objects.create(**validated_data)
        for m in medicines_data:
            PrescriptionMedicine.objects.create(prescription=prescription, **m)
        return prescription

    def update(self, instance, validated_data):
        medicines_data = validated_data.pop('medicines', None)
        # update normal fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if medicines_data is not None:
            # Simple strategy: delete all and recreate (safe, small datasets).
            # Optionally implement upsert logic using 'id' field.
            instance.medicines.all().delete()
            for m in medicines_data:
                PrescriptionMedicine.objects.create(prescription=instance, **m)
        return instance
