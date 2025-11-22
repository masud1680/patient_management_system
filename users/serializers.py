# from rest_framework import serializers
# from .models import PatientProfile, DoctorProfile

# class PatientProfileSerializer(serializers.ModelSerializer):
#     user_email = serializers.EmailField(source="user.email", read_only=True)
    
#     class Meta:
#         model = PatientProfile
#         fields = [
#             "id",
#             "user",
#             "user_email",
#             "gender",
#             "phone_number",
#             "blood_group",
#             "age",
#             "address",
#             "short_bio",
#             "visible_to_doctors",
#         ]

# class DoctorProfileSerializer(serializers.ModelSerializer):
#     user_email = serializers.EmailField(source="user.email", read_only=True)

#     class Meta:
#         model = DoctorProfile
#         fields = [
#             "id",
#             "user",
#             "user_email",
#             "gender",
#             "age",
#             "qualification",
#             "specialization",
#             "address",
#             "short_bio",
#             "phone_number",
#             "available_days",
#             "available_time"
#         ]
