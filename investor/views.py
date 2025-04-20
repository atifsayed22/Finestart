from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from startup.models import Startup, Offer  # Import the Startup and Offer models
from accounts.models import InvestorProfile
from django.contrib import messages

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
    # Check if user is an investor
    if request.user.user_type.lower() != 'investor':
        from django.contrib import messages
        messages.warning(request, "This page is only for investor users.")
        return redirect('home')
        
    try:
        # Get all startups with their documents
        startups = Startup.objects.all().select_related('user')
        
        # Get filter parameters
        industry = request.GET.get('industry')
        years_range = request.GET.get('years')
        growth_trend = request.GET.get('growth')
        score_range = request.GET.get('score')
        risk_level = request.GET.get('risk')
        
        # Apply filters if they are provided
        if industry:
            startups = startups.filter(industry_type=industry)
        
        if years_range:
            if years_range == '0-1':
                startups = startups.filter(years_in_business__lt=1)
            elif years_range == '1-3':
                startups = startups.filter(years_in_business__gte=1, years_in_business__lt=3)
            elif years_range == '3-5':
                startups = startups.filter(years_in_business__gte=3, years_in_business__lt=5)
            elif years_range == '5+':
                startups = startups.filter(years_in_business__gte=5)
        
        if growth_trend:
            startups = startups.filter(growth_trend=growth_trend)
        
        # Import the scoring and risk assessment functions from startup views
        from startup.views import calculate_startup_score, assess_startup_risk
        
        # Prepare startup data with documents for display
        startup_data = []
        
        # First pass to get scores and risk assessments
        startups_with_scores = []
        for startup in startups:
            try:
                # Get the startup profile if it exists
                from accounts.models import StartupProfile
                startup_profile = StartupProfile.objects.get(user=startup.user)
                
                # Calculate score and risk assessment
                score = calculate_startup_score(startup, startup_profile)
                risk_assessment = assess_startup_risk(startup, startup_profile)
                
                # Apply score filter if specified
                if score_range:
                    min_score, max_score = map(int, score_range.split('-'))
                    if not (min_score <= score <= max_score):
                        continue
                
                # Apply risk filter if specified
                if risk_level and risk_assessment != risk_level:
                    continue
                
                # Add score and risk to startup object
                startup.score = score
                startup.risk_assessment = risk_assessment
                
                startups_with_scores.append(startup)
            except StartupProfile.DoesNotExist:
                # Skip startups without profiles
                continue
        
        # Sort by score (highest first)
        startups_with_scores.sort(key=lambda x: x.score, reverse=True)
        
        # Build the final data structure
        for startup in startups_with_scores:
            startup_info = {
                'startup': startup,
                'has_pitch': bool(startup.pitch_video),
                'has_proposal': bool(startup.business_proposal),
                'has_legal_docs': bool(startup.legal_documents),
                'has_logo': bool(startup.company_logo),
                'score': startup.score,
                'risk_assessment': startup.risk_assessment
            }
            startup_data.append(startup_info)
        
        # Prepare context with filter options
        context = {
            'startup_data': startup_data,
            'filter_options': {
                'industry': industry,
                'years_range': years_range,
                'growth_trend': growth_trend,
                'score_range': score_range,
                'risk_level': risk_level
            }
        }
        
        return render(request, 'investor/startup_discovery.html', context)
    except Exception as e:
        # Handle errors
        from django.contrib import messages
        messages.error(request, f"Error loading startup data: {str(e)}")
        return render(request, 'investor/startup_discovery.html', {'startup_data': []})

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

# Redirect from older find_startups view to the consolidated startup_discovery view
@login_required
def find_startups(request):
    messages.info(request, "You've been redirected to our enhanced startup discovery page.")
    return redirect('investor:startup_discovery')
