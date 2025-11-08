from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

def is_admin(user):
    return user.groups.filter(name="admin").exists()

def is_doctor(user):
    return user.groups.filter(name="doctor").exists()

def is_patient(user):
    return user.groups.filter(name="patient").exists()

def RegisterView(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_data_has_error = False

        if User.objects.filter(username=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')
        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email, 
                username=email,
                password=password
                
            )
            new_user.is_active = False
            new_user.save()
            
            messages.success(request, "Account created. Check your mail & active your account.")
            return redirect('login')

    return render(request, 'auth/register.html')

def ActiveAccountView(request, user_id, token):
    try:
        user = User.objects.get(id = user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            messages.success(request, "Account activated.")
        else:
            return HttpResponse('Token Invalid!!')
    except user.DoesNotExist:
        return HttpResponse('User does not exist!!')
            
    return redirect('login')

def LoginView(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('dashboard')
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'auth/login.html')

def LogoutView(request):

    logout(request)

    return redirect('login')

def ForgotPassword(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            # full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'
            full_password_reset_url = f'{settings.FONTEND_URL}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'auth/forgot_password.html')

def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'auth/password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'auth/reset_password.html') 

@login_required
def patient_dashboard(request):

    return render(request, 'users_dashboard/patient_dashboard.html')

@login_required
def doctor_dashboard(request):

    return render(request, 'users_dashboard/doctor_dashboard.html')

def redirect_dashboard(request):
    
    if is_patient(request.user):
        return redirect('patient-dashboard')
    
    elif is_doctor(request.user):
        return redirect('doctor-dashboard')
    
    elif is_admin(request.user):
        return redirect('admin-dashboard')
    
    else :
        return redirect('no-permission')