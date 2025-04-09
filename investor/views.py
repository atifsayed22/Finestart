from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from startup.models import Startup  # Import the Startup model
from accounts.models import InvestorProfile

# Create your views here.

@login_required
def investor_dashboard(request):
    # You might want to pass investor-specific data here later
    return render(request, 'investor/investor_dashboard.html')

@login_required
def startup_discovery(request):
    startups = Startup.objects.all()  # Query all startups
    
    # --- Debugging Start ---
    print("--- Startups QuerySet ---")
    for s in startups:
        print(f"ID: {s.id}, Name: {s.name}")
    print("--- End Startups QuerySet ---")
    # --- Debugging End ---

    # Add filtering logic here based on search criteria later if needed
    context = {
        'startups': startups
    }
    return render(request, 'investor/startup_discovery.html', context)

@login_required
def portfolio_tracker(request):
    # You might want to pass portfolio data here later
    return render(request, 'investor/portfolio_tracker.html')

@login_required
def investor_profile(request):
    try:
        investor = InvestorProfile.objects.get(user=request.user)
    except InvestorProfile.DoesNotExist:
        investor = None
    
    context = {
        'investor': investor
    }
    return render(request, 'investor/investor_profile.html', context)
