from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string, constant_time_compare

from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']  # Get the identifier from the form
            password = form.cleaned_data['password']
            
            if '@' in identifier:
                user = CustomUser.objects.get(email=identifier)
                identifier = user.username
            
            user = authenticate(request, username=identifier, password=password)

            if user is not None:
                if user.is_verified:
                    if user.is_approved:
                        if user.is_active:
                            login(request, user)
                            return redirect('core:home')
                        else:
                            messages.error(request, 'Your account is inactive. Please contact the administrator.')
                    else:
                        messages.error(request, 'Your account is unapproved. Please contact the administrator.')
                else:
                    messages.error(request, 'Your account is unverified. Please verify your account.')
            else:
                messages.error(request, 'Invalid username, email, or password.')
        else:
            # If the form is not valid, re-render the form with errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = LoginForm()
    
    return render(request, 'user/login.html', {'form': form})

#registration process

def register(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            user.email_verification_token = token
            user.email_verification_sent_at = timezone.now()
            user.save()

            send_verification_email(user)
            return redirect('account:verification_sent')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'user/register.html', {'form': form})

def send_verification_email(user):
    subject = 'Verify your email address'
    token = user.email_verification_token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"http://127.0.0.1:8000/account/verify-email/{uid}/{token}/"
    message = f'Click the following link to verify your email address: {verification_url}'
    send_mail(subject, message, 'sender@example.com', [user.email])

def verification_sent(request):
    return render(request, 'user/verification_sent.html')

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if user.is_verified:
                messages.success(request, 'Email already verified.')
            else:
                user.is_verified = True
                user.save()
                messages.success(request, 'Email verified successfully.')
            return redirect('account:verification_success')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('account:verification_failed')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('account:verification_failed')

def verification_failed(request):
    return render(request, 'user/verification_failed.html')

def verification_success(request):
    return render(request, 'user/verification_success.html')

## end registraiton

def reset_password(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'user/reset_password.html')

def confirm_password(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'user/confirm_password.html')

def new_password(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    return render(request, 'user/new_password.html')

@login_required
def logout(request):
    if request.method=="POST":
        auth.logout(request)
        return redirect('account:login')