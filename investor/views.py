from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from startup.models import Startup, Offer  # Import the Startup and Offer models
from accounts.models import InvestorProfile

# Create your views here.

@login_required
def investor_dashboard(request):
    # Check if user is an investor
    if request.user.user_type.lower() != 'investor':
        # Redirect non-investor users to home
        from django.contrib import messages
        messages.warning(request, "This page is only for investor users.")
        return redirect('home')
        
    context = {}
    
    # Try to get investor profile
    try:
        investor_profile = InvestorProfile.objects.get(user=request.user)
        context['investor'] = investor_profile
        
        # Get offers made by this investor
        offers = Offer.objects.filter(investor=investor_profile).order_by('-created_at')
        context['offers'] = offers
        
        # Count offers by status
        pending_count = offers.filter(status='pending').count()
        accepted_count = offers.filter(status='accepted').count()
        rejected_count = offers.filter(status='rejected').count()
        
        context['offer_counts'] = {
            'pending': pending_count,
            'accepted': accepted_count,
            'rejected': rejected_count,
            'total': offers.count()
        }
        
    except InvestorProfile.DoesNotExist:
        context['profile_missing'] = True
    except Exception as e:
        # Log error but don't crash
        print(f"Error in investor_dashboard: {e}")
        context['error'] = str(e)
    
    # Add welcome message
    if request.user.is_authenticated:
        welcome_name = request.user.first_name if request.user.first_name else request.user.username
        context['welcome_name'] = welcome_name
    
    return render(request, 'investor/investor_dashboard.html', context)

@login_required
def startup_discovery(request):
    startups = Startup.objects.all()  # Query all startups

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
    # First check if user is investor type
    if request.user.user_type.lower() != 'investor':
        from django.contrib import messages
        messages.warning(request, "This profile page is only for investor users.")
        return redirect('home')
        
    if request.method == 'POST':
        # Handle profile creation/update
        try:
            # Get or create the profile
            investor, created = InvestorProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'investor_type': request.POST.get('investor_type', 'Individual'),
                    'investment_range': request.POST.get('investment_range', '0-50000'),
                    'bio': request.POST.get('bio', ''),
                    'company_name': request.POST.get('company_name', ''),
                    'investment_focus': request.POST.get('investment_focus', ''),
                    'portfolio_size': int(request.POST.get('portfolio_size', 0)),
                    'location': request.POST.get('location', '')
                }
            )
            
            if not created:
                # Update existing profile
                investor.investor_type = request.POST.get('investor_type', investor.investor_type)
                investor.investment_range = request.POST.get('investment_range', investor.investment_range)
                investor.bio = request.POST.get('bio', investor.bio)
                investor.company_name = request.POST.get('company_name', investor.company_name)
                investor.investment_focus = request.POST.get('investment_focus', investor.investment_focus)
                investor.portfolio_size = int(request.POST.get('portfolio_size', investor.portfolio_size))
                investor.location = request.POST.get('location', investor.location)
                investor.save()
                
            # Handle profile picture upload
            if 'profile_picture' in request.FILES:
                investor.profile_picture = request.FILES['profile_picture']
                investor.save()
                
            # Handle company logo upload
            if 'company_logo' in request.FILES:
                investor.company_logo = request.FILES['company_logo']
                investor.save()
                
            from django.contrib import messages
            if created:
                messages.success(request, "Investor profile created successfully!")
            else:
                messages.success(request, "Investor profile updated successfully!")
                
            return redirect('investor:investor_dashboard')
            
        except Exception as e:
            print(f"Error creating/updating investor profile: {e}")
            from django.contrib import messages
            messages.error(request, f"Error saving profile: {str(e)}")
    
    # GET request - show the profile or form
    try:
        investor = InvestorProfile.objects.get(user=request.user)
        # Profile exists, show the profile view
    except InvestorProfile.DoesNotExist:
        # No profile yet, set to None to show the creation form
        investor = None
    
    context = {
        'investor': investor
    }
    return render(request, 'investor/investor_profile.html', context)
