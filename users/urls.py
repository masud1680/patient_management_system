from django.urls import path, include
from users.views import  RegisterView, ActiveAccountView ,LoginView, LogoutView, ForgotPassword, PasswordResetSent, ResetPassword, redirect_dashboard, patient_dashboard, doctor_dashboard
# from rest_framework.routers import DefaultRouter
# from .views import PatientProfileViewSet, DoctorProfileViewSet

# router = DefaultRouter()
# router.register('patients', PatientProfileViewSet)
# router.register('doctors', DoctorProfileViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('register/', RegisterView, name='register'),
    path('activate/<int:user_id>/<str:token>/', ActiveAccountView , ),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),

    path('forgot-password/', ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', ResetPassword, name='reset-password'),

    # users dashboard

    path('dashboard/', redirect_dashboard, name="dashboard"),
    path('patient-dashboard/', patient_dashboard, name="patient-dashboard"),
    path('doctor-dashboard/', doctor_dashboard, name="doctor-dashboard"),
]
