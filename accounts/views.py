from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm
from .models import StartupProfile, InvestorProfile, CustomUser

def signup(request):
    if request.method == "POST":
        try:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    # Log the user in after signup
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, "Signup successful! Welcome to FineStart.")
                        return redirect("login")
                    else:
                        messages.warning(request, "Account created but auto-login failed. Please log in manually.")
                        return redirect("login")
                except Exception as e:
                    print(f"Error during signup process: {e}")
                    messages.error(request, f"Error during signup: {str(e)}")
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as outer_e:
            print(f"Unexpected error in signup view: {outer_e}")
            messages.error(request, "An unexpected error occurred. Please try again.")
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
            # Include the username in the welcome message
            welcome_name = user.first_name if user.first_name else user.username
            messages.success(request, f"Login successful! Welcome, {welcome_name}!")
            
            # Check user type and redirect accordingly
            try:
                if user.user_type.lower() == "startup":
                    # Check if user has a startup profile
                    if StartupProfile.objects.filter(user=user).exists():
                        return redirect("startup:startup_dashboard")
                    else:
                        return redirect("startup:startup_profile")
                else:
                    # For investor users
                    if InvestorProfile.objects.filter(user=user).exists():
                        return redirect("investor:investor_dashboard")
                    else:
                        # Redirect to investor profile creation page
                        return redirect("investor:investor_profile")
            except Exception as e:
                # If any error occurs, check user type for redirection
                print(f"Error checking user profile: {e}")
                if user.user_type.lower() == "investor":
                    return redirect("investor:investor_dashboard")
                else:
                    return redirect("startup:startup_dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")

def startup_profile(request):
    # Redirect to the startup app's profile view with the namespace to avoid ambiguity
    return redirect('startup:startup_profile')