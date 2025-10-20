from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SignupForm
from .models import Profile
from django.db import transaction

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            with transaction.atomic():  # Ensures database safety
                user = form.save()

                # Create profile only if it doesn’t exist
                Profile.objects.get_or_create(user=user)

                messages.success(request, "✅ Account created successfully! You can now log in.")
                return redirect('login')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('dashboard_home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')
