from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def investor_dashboard(request):
    return render(request, 'investor/investor_dashboard.html')

@login_required
def startup_discovery(request):
    return render(request, 'investor/startup_discovery.html')

@login_required
def portfolio_tracker(request):
    return render(request, 'investor/portfolio_tracker.html')
