from django.urls import path
from users.views import  RegisterView, ActiveAccountView ,LoginView, LogoutView, ForgotPassword, PasswordResetSent, ResetPassword

urlpatterns = [
    
    path('register/', RegisterView, name='register'),
    path('activate/<int:user_id>/<str:token>/', ActiveAccountView , ),
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),

    path('forgot-password/', ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', ResetPassword, name='reset-password'),
]
