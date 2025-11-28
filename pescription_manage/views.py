# core/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from .models import PatientProfile, DoctorProfile, Prescription
from .serializers import PatientProfileSerializer, DoctorProfileSerializer, PrescriptionSerializer
from .permissions import IsDoctor, IsPatient, IsDoctorOrReadOnly


class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.select_related('user').all()
    serializer_class = PatientProfileSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsDoctor])
    def search(self, request):
        # search by email query param ?q=
        q = request.query_params.get('q', '').strip()
        if not q:
            return Response({"detail": "Provide query param 'q' (email or name)."}, status=400)
        patients = self.queryset.filter(
            Q(user__email__icontains=q) | Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q)
        )
        serializer = self.get_serializer(patients, many=True)
        return Response(serializer.data)

# DoctorProfile viewset (read-only)
class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.select_related('user').all()
    serializer_class = DoctorProfileSerializer

# Prescription viewset
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('patient__user','doctor__user').prefetch_related('medicines').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsDoctorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # If doctor -> show all prescriptions for patients who allow visibility, plus their own created ones
        if hasattr(user, 'doctorprofile'):
            # show prescriptions of patients where visible_to_doctors True OR prescriptions created by this doctor
            return self.queryset.filter(
                Q(patient__visible_to_doctors=True) | Q(doctor=user.doctorprofile)
            ).distinct()
        # If patient -> show only their prescriptions
        if hasattr(user, 'patientprofile'):
            return self.queryset.filter(patient=user.patientprofile)
        # else empty
        return self.queryset.none()

    def perform_create(self, serializer):
        # if request.user is doctor, set doctor automatically
        user = self.request.user
        doc = getattr(user, 'doctorprofile', None)
        if doc and 'doctor' not in serializer.validated_data:
            serializer.save(doctor=doc)
        else:
            serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsDoctor])
    def upload_image(self, request, pk=None):
        prescription = self.get_object()
        file = request.FILES.get('image')
        if not file:
            return Response({"detail":"No file uploaded under 'image'."}, status=400)
        prescription.image = file
        prescription.save()
        return Response(self.get_serializer(prescription).data)

    @action(detail=True, methods=['get'], permission_classes=[IsDoctorOrReadOnly])
    def print(self, request, pk=None):
        """
        Returns a rendered HTML of the prescription (suitable for printing).
        Optionally you can accept ?format=pdf to return PDF (requires extra lib)
        """
        prescription = self.get_object()
        # check patient visibility for doctors
        if hasattr(request.user, 'doctorprofile') and not prescription.patient.visible_to_doctors and prescription.doctor != request.user.doctorprofile:
            return Response({"detail":"Patient has hidden prescriptions."}, status=403)

        medicines = prescription.medicines.all()
        ctx = {
            "prescription": prescription,
            "medicines": medicines,
        }

        fmt = request.query_params.get('format', 'html').lower()
        if fmt == 'html':
            # Render HTML template (you must create the template)
            return render(request, 'prescriptions/print.html', ctx)
        elif fmt == 'pdf':
            # Optional PDF generation using WeasyPrint or xhtml2pdf.
            # We'll provide example using WeasyPrint (install weasyprint and dependencies).
            try:
                from weasyprint import HTML
            except Exception:
                return Response({"detail":"PDF generation not available. Install weasyprint."}, status=501)
            html_string = render(request, 'prescriptions/print.html', ctx).content.decode('utf-8')
            pdf = HTML(string=html_string).write_pdf()
            response = Response(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename=prescription_{prescription.id}.pdf'
            return response
        else:
            return Response({"detail":"Unknown format. Use ?format=html or ?format=pdf"}, status=400)



class PrescriptionCountSingle(APIView):

    def get(self, request):
        patient_id = request.GET.get("patient_id")


        if not patient_id:
            return Response({"error": "patient_id required"}, status=400)

        count = Prescription.objects.filter(patient_id=patient_id).count()

        return Response({
            "patient_id": patient_id,
            "total_prescriptions": count
        })



class UniqueDoctorsForPatient(APIView):
    def get(self, request):
        patient_id = request.GET.get("patient_id")

        if not patient_id:
            return Response({"error": "patient_id required"}, status=400)

        # Find unique doctors for this patient
        doctors = Prescription.objects.filter(
            patient_id=patient_id
        ).values_list("doctor_id", flat=True).distinct()

        return Response({
            "patient_id": patient_id,
            "unique_doctor_count": len(doctors),
            "doctor_ids": list(doctors)
        })




class UniqueDoctorDetailsForPatient(APIView):
    def get(self, request):
        patient_id = request.GET.get("patient_id")

        if not patient_id:
            return Response({"error": "patient_id required"}, status=400)

        # get unique doctor IDs
        doctor_ids = Prescription.objects.filter(
            patient_id=patient_id
        ).values_list("doctor_id", flat=True).distinct()

        # fetch doctor details
        doctors = DoctorProfile.objects.filter(id__in=doctor_ids)

        doctor_data = []
        for d in doctors:
            doctor_data.append({
                "id": d.id,
                "name": d.user.get_full_name(),
                "email": d.user.email,
                "qualification": d.qualification,
                "specialization": d.specialization,
                "phone_number": d.phone_number,
                "available_days": d.available_days,
                "available_time": d.available_time,

            })

        return Response({
            "patient_id": patient_id,
            "unique_doctor_count": len(doctor_data),
            "doctors": doctor_data
        })
