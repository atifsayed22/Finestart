from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm
from .models import StartupProfile, InvestorProfile, CustomUser

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after signup
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "Signup successful! Welcome to FineStart.")
            return redirect("login")  # Redirect to homepage after successful signup
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            
            # Check user type and redirect accordingly
            user_profile = CustomUser.objects.get(username=username)
            if user_profile.user_type.lower() == "startup":
                return redirect("startup_dashboard")
            else:
                return redirect("investor_dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")

def startup_profile(request):
    return redirect(reverse('startup_registration'))