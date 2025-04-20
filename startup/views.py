from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Startup, Offer
from accounts.models import InvestorProfile, CustomUser, StartupProfile, MonthlyProfit
import json
from django.views.decorators.http import require_POST
from datetime import datetime

@login_required
def startup_registration(request):
    try:
        # Check if the user already has both a profile and a startup
        if StartupProfile.objects.filter(user=request.user).exists() and Startup.objects.filter(user=request.user).exists():
            messages.info(request, "You have already registered your startup.")
            return redirect('startup:startup_dashboard')
    except Exception as e:
        print(f"Error checking for existing profile and startup: {e}")
    
    if request.method == 'POST':
        try:
            print("Registration submission received")
            print(f"POST data: {request.POST}")
            print(f"FILES data: {request.FILES}")
            
            name = request.POST.get('startup-name', '')
            industry_type = request.POST.get('industry-type', '')
            years_in_business = request.POST.get('years-in-business', 0)
            
            if not name:
                raise ValueError("Startup name is required")
            
            if not industry_type:
                raise ValueError("Industry type is required")
            
            try:
                annual_revenue = float(request.POST.get('revenue', 0))
            except (ValueError, TypeError):
                annual_revenue = 0
                
            try:
                profit_margin = float(request.POST.get('profit-margin', 0))
            except (ValueError, TypeError):
                profit_margin = 0
                
            try:
                investment_required = float(request.POST.get('investment-required', 0))
            except (ValueError, TypeError):
                investment_required = 0
            
            funding_purpose = request.POST.get('funding-purpose', '')
            target_market = request.POST.get('target-market', '')
            growth_trend = request.POST.get('growth-trend', '')
            
            company_logo = request.FILES.get('company-logo') if 'company-logo' in request.FILES else None
            pitch_video = request.FILES.get('pitch-video') if 'pitch-video' in request.FILES else None
            business_proposal = request.FILES.get('business-proposal') if 'business-proposal' in request.FILES else None
            legal_documents = request.FILES.get('legal-documents') if 'legal-documents' in request.FILES else None
            
            startup = Startup(
                user=request.user,  # Ensure user is assigned
                name=name,
                industry_type=industry_type,
                years_in_business=years_in_business,
                company_logo=company_logo,
                annual_revenue=annual_revenue,
                profit_margin=profit_margin,
                investment_required=investment_required,
                funding_purpose=funding_purpose,
                target_market=target_market,
                growth_trend=growth_trend,
                pitch_video=pitch_video,
                business_proposal=business_proposal,
                legal_documents=legal_documents
            )
            startup.save()
            
            try:
                # Get or create the startup profile
                startup_profile, created = StartupProfile.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'startup_name': name,
                        'industry': industry_type,
                        'monthly_profit': profit_margin
                    }
                )
                
                # Set the profile picture to be the same as the company logo if it exists
                if company_logo and not startup_profile.profile_picture:
                    startup_profile.profile_picture = company_logo
                    startup_profile.save()
                    
            except Exception as profile_error:
                print(f"Could not create startup profile: {profile_error}")
            
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': 'Startup registered successfully!',
                    'redirect_url': '/startup/dashboard/'
                })
            else:
                messages.success(request, 'Startup registered successfully!')
                return redirect('startup:startup_dashboard')
            
        except Exception as e:
            error_message = str(e)
            print(f"Error in startup registration: {error_message}")
            
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': f"Error: {error_message}"
                }, status=400)
            else:
                messages.error(request, error_message)
                return redirect('startup:startup_registration')
    
    return render(request, 'forms.html')


def startup_dashboard(request):
    # Initialize context dictionary
    context = {}
    
    # First, check if the user is authenticated and is a startup user type
    if not request.user.is_authenticated or request.user.user_type.lower() != 'startup':
        messages.warning(request, "This page is only for startup users.")
        return redirect('home')
    
    try:
        # Check if the user has a startup record first
        startup_exists = Startup.objects.filter(user=request.user).exists()
        
        # If no startup record exists, redirect to registration regardless of profile
        if not startup_exists:
            messages.info(request, "Please register your startup to access your dashboard.")
            return redirect('startup:startup_registration')
            
        # Now check if the user has a startup profile
        try:
            profile = StartupProfile.objects.get(user=request.user)
            context['profile'] = profile
            
            # Get the startup
            startup = Startup.objects.get(user=request.user)
            context['startup'] = startup
            
            # Get pending offers
            pending_offers = Offer.objects.filter(startup=startup, status='pending').order_by('-created_at')
            context['pending_offers'] = pending_offers
            context['offer_count'] = pending_offers.count()
            
            # Get accepted and all offers for statistics
            accepted_offers = Offer.objects.filter(startup=startup, status='accepted')
            all_offers = Offer.objects.filter(startup=startup)
            context['accepted_offers'] = accepted_offers
            context['total_offers'] = all_offers.count()
            
            # Get profit data for the chart
            profit_data = profile.get_monthly_profits(months=6)
            context['profit_labels'] = json.dumps(profit_data['labels'])
            context['profit_values'] = json.dumps(profit_data['values'])
            
        except StartupProfile.DoesNotExist:
            # If no profile exists but startup exists, create minimal profile
            # This is an edge case that shouldn't happen with normal flow
            messages.info(request, "Please complete your startup profile to access all features.")
            return redirect('startup:startup_profile')

    except Exception as e:
        print(f"Error getting startup profile for dashboard: {e}")
        context['error'] = str(e)
        messages.error(request, "There was an error loading your dashboard. Please try again.")
        return redirect('startup:startup_registration')
    
    # Pass the welcome message to the template
    if request.user.is_authenticated:
        welcome_name = request.user.first_name if request.user.first_name else request.user.username
        context['welcome_name'] = welcome_name
        
    return render(request, 'startup/startup_dashboard.html', context)

@login_required
def profit_data(request):
    try:
        # Get the startup profile for the current user
        profile = StartupProfile.objects.get(user=request.user)
        
        # Get the profit entries for this startup
        profit_entries = MonthlyProfit.objects.filter(startup=profile).order_by('date')
        
        # Format data for the chart
        profit_data = []
        for entry in profit_entries:
            formatted_date = entry.date.strftime('%b %Y')  # Format: 'Jan 2023'
            profit_data.append({
                'date': formatted_date,
                'amount': float(entry.amount)
            })
        
        return JsonResponse({
            'success': True,
            'profit_data': profit_data
        })
    except StartupProfile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'No startup profile found for this user'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def startup_insights(request):
    try:
        # Check if this is an investor viewing a specific startup's insights
        startup_id = request.GET.get('startup_id')
        is_investor_view = request.user.user_type.lower() == 'investor' and startup_id
        
        # First check if startup exists before proceeding
        if is_investor_view:
            # For investor view
            startup = get_object_or_404(Startup, id=startup_id)
            
            # For investors, only show insights for complete startup profiles
            if not StartupProfile.objects.filter(user=startup.user).exists():
                messages.warning(request, "This startup doesn't have a complete profile yet.")
                return redirect('investor:startup_discovery')
                
            profile = StartupProfile.objects.get(user=startup.user)
        else:
            # For startup owner view
            # First check if the startup record exists
            if not Startup.objects.filter(user=request.user).exists():
                messages.warning(request, "Please complete your startup registration first.")
                return redirect('startup:startup_registration')
                
            # Then check if the profile exists
            if not StartupProfile.objects.filter(user=request.user).exists():
                messages.warning(request, "Please complete your startup profile first.")
                return redirect('startup:edit_profile')
                
            # If both exist, get them
            profile = StartupProfile.objects.get(user=request.user)
            startup = Startup.objects.get(user=request.user)
        
        # Calculate startup score (0-100)
        score = calculate_startup_score(startup, profile)
        
        # Calculate score breakdown
        score_breakdown = {
            'info_score': calculate_info_score(startup, profile),
            'financial_score': calculate_financial_score(startup, profile),
            'maturity_score': calculate_maturity_score(startup, profile),
            'team_score': calculate_team_score(profile),
            'market_score': calculate_market_score(startup, profile)
        }
        
        # Calculate percentages for progress bars
        score_breakdown['info_percent'] = (score_breakdown['info_score'] / 20) * 100
        score_breakdown['financial_percent'] = (score_breakdown['financial_score'] / 30) * 100
        score_breakdown['maturity_percent'] = (score_breakdown['maturity_score'] / 25) * 100
        score_breakdown['team_percent'] = (score_breakdown['team_score'] / 10) * 100
        score_breakdown['market_percent'] = (score_breakdown['market_score'] / 15) * 100
        
        # Calculate risk assessment
        risk_assessment = assess_startup_risk(startup, profile)
        
        # Get profit data for charts
        profit_data = profile.get_monthly_profits(months=12)
        
        context = {
            'profile': profile,
            'startup': startup,
            'score': score,
            'score_breakdown': score_breakdown,
            'risk_assessment': risk_assessment,
            'profit_labels': json.dumps(profit_data['labels']),
            'profit_values': json.dumps(profit_data['values']),
            'is_investor_view': is_investor_view,
        }
        return render(request, 'startup/startup_insights.html', context)
    except StartupProfile.DoesNotExist:
        if request.user.user_type.lower() == 'investor':
            messages.warning(request, "This startup doesn't have a complete profile yet.")
            return redirect('investor:startup_discovery')
        else:
            messages.warning(request, "Please complete your startup profile first.")
            return redirect('startup:edit_profile')
    except Startup.DoesNotExist:
        if request.user.user_type.lower() == 'investor':
            messages.warning(request, "This startup doesn't exist or has been removed.")
            return redirect('investor:startup_discovery')
        else:
            messages.warning(request, "Please complete your startup registration first.")
            return redirect('startup:startup_registration')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        if request.user.user_type.lower() == 'investor':
            return redirect('investor:startup_discovery')
        else:
            return redirect('startup:startup_dashboard')

def calculate_info_score(startup, profile):
    """Calculate score for information quality (max 20 points)"""
    score = 0
    
    # Quality of company description
    if profile.company_description and len(profile.company_description) > 100:
        score += 10
    elif profile.company_description:
        score += 5
    
    # Profile picture
    if profile.profile_picture:
        score += 5
    
    # Pitch video
    if startup.pitch_video:
        score += 5
    
    return min(20, score)

def calculate_financial_score(startup, profile):
    """Calculate score for financial metrics (max 30 points)"""
    score = 0
    
    # Revenue
    if startup.annual_revenue > 0:
        revenue_score = min(15, startup.annual_revenue / 100000)
        score += revenue_score
    
    # Profit margin
    if startup.profit_margin > 0:
        margin_score = min(15, startup.profit_margin * 0.15)
        score += margin_score
    
    return min(30, int(score))

def calculate_maturity_score(startup, profile):
    """Calculate score for business maturity (max 25 points)"""
    score = 0
    
    # Years in business
    if startup.years_in_business > 0:
        years_score = min(15, startup.years_in_business * 3)
        score += years_score
    
    # Business model clarity
    if profile.business_model:
        score += 5
    
    # Equity structure
    if profile.equity_structure:
        score += 5
    
    return min(25, int(score))

def calculate_team_score(profile):
    """Calculate score for team (max 10 points)"""
    score = 0
    
    # Team size
    if profile.team_size > 0:
        team_score = min(10, profile.team_size)
        score += team_score
    
    return min(10, int(score))

def calculate_market_score(startup, profile):
    """Calculate score for market factors (max 15 points)"""
    score = 0
    
    # Target market clarity
    if startup.target_market:
        score += 5
    
    # Growth trend
    if startup.growth_trend == 'rapid':
        score += 10
    elif startup.growth_trend == 'steady':
        score += 5
    
    return min(15, int(score))

def calculate_startup_score(startup, profile):
    """Calculate a score from 0-100 based on various factors"""
    # Combine all score components
    info_score = calculate_info_score(startup, profile)
    financial_score = calculate_financial_score(startup, profile)
    maturity_score = calculate_maturity_score(startup, profile)
    team_score = calculate_team_score(profile)
    market_score = calculate_market_score(startup, profile)
    
    # Sum all scores
    total_score = info_score + financial_score + maturity_score + team_score + market_score
    
    return min(100, int(total_score))

def assess_startup_risk(startup, profile):
    """Assess risk level for investors (Low, Medium, High)"""
    risk_factors = 0
    
    # Financial risk factors
    if startup.annual_revenue < 10000:
        risk_factors += 2
    elif startup.annual_revenue < 50000:
        risk_factors += 1
    
    if startup.profit_margin <= 0:
        risk_factors += 2
    elif startup.profit_margin < 0.1:  # less than 10%
        risk_factors += 1
    
    # Business maturity factors
    if startup.years_in_business < 1:
        risk_factors += 2
    elif startup.years_in_business < 3:
        risk_factors += 1
    
    # Market factors
    if startup.growth_trend == 'declining':
        risk_factors += 2
    elif startup.growth_trend == 'stable':
        risk_factors += 1
    
    # Team factors
    if profile.team_size < 3:
        risk_factors += 1
    
    # Determine risk level
    if risk_factors >= 6:
        return 'High'
    elif risk_factors >= 3:
        return 'Medium'
    else:
        return 'Low'

@login_required
def startup_profile(request):
    # Handle potential database errors
    try:
        # Check if the user already has a profile
        try:
            profile = StartupProfile.objects.get(user=request.user)
            
            # Get associated startup model for documents
            try:
                startup = Startup.objects.get(user=request.user)
                has_startup = True
            except Startup.DoesNotExist:
                startup = None
                has_startup = False
                
            # Get profit data for the chart
            profit_data = profile.get_monthly_profits(months=6)
            
            # If profile exists, show the profile view
            return render(request, 'startup/profile_view.html', {
                'profile': profile,
                'startup': startup,
                'has_startup': has_startup,
                'profit_data': {
                    'labels': profit_data['labels'],
                    'values': profit_data['values']
                }
            })
        except StartupProfile.DoesNotExist:
            # If no profile exists and it's a POST request, create a new profile
            if request.method == 'POST':
                try:
                    monthly_profit = float(request.POST.get('monthly_profit', 0))
                    profit_margin = float(request.POST.get('profit_margin', 10))
                    
                    # Create the profile with all form data
                    profile = StartupProfile(
                        user=request.user,
                        startup_name=request.POST.get('startup-name', ''),
                        industry=request.POST.get('industry', ''),
                        team_size=int(request.POST.get('team_size', 1)),
                        ceo_name=request.POST.get('ceo_name', ''),
                        startup_stage=request.POST.get('startup_stage', ''),
                        equity_structure=request.POST.get('equity_structure', ''),
                        business_model=request.POST.get('business_model', ''),
                        company_description=request.POST.get('company_description', ''),
                        monthly_profit=monthly_profit,
                        # Contact information
                        website=request.POST.get('website', ''),
                        contact_email=request.POST.get('contact_email', request.user.email),
                        phone_number=request.POST.get('phone_number', ''),
                        location=request.POST.get('location', ''),
                        country=request.POST.get('country', '')
                    )
                    
                    # Handle profile picture upload
                    if 'profile_picture' in request.FILES:
                        profile.profile_picture = request.FILES['profile_picture']
                        
                    profile.save()
                    
                    # Create or update associated Startup entry for investor visibility
                    try:
                        startup, created = Startup.objects.get_or_create(
                            user=request.user,
                            defaults={
                                'name': profile.startup_name,
                                'industry_type': profile.industry,
                                'years_in_business': 1,  # Default value
                                'annual_revenue': profile.monthly_profit * 12,
                                'profit_margin': profit_margin,  # Get profit margin as percentage
                                'investment_required': float(request.POST.get('investment_required', 50000)),
                                'funding_purpose': profile.company_description or "Funding details not specified",
                                'target_market': request.POST.get('target_market', "Target market not specified"),
                                'growth_trend': request.POST.get('growth_trend', "stable")  # Default value
                            }
                        )
                        
                        # Always sync the company logo/profile picture
                        if 'profile_picture' in request.FILES:
                            startup.company_logo = request.FILES['profile_picture']
                            
                        # Handle business documents upload
                        if 'business_proposal' in request.FILES:
                            startup.business_proposal = request.FILES['business_proposal']
                            
                        if 'legal_documents' in request.FILES:
                            startup.legal_documents = request.FILES['legal_documents']
                            
                        if 'pitch_video' in request.FILES:
                            startup.pitch_video = request.FILES['pitch_video']
                            
                        startup.save()
                    except Exception as startup_error:
                        print(f"Error syncing with Startup model: {startup_error}")
                    
                    # Create monthly profit record
                    try:
                        from accounts.models import MonthlyProfit
                        from django.utils import timezone
                        import datetime
                        
                        # Create current month's profit record 
                        today = timezone.now().date()
                        current_month = datetime.date(today.year, today.month, 1)
                        
                        MonthlyProfit.objects.create(
                            startup=profile,
                            date=current_month,
                            amount=monthly_profit
                        )
                        
                        # Create some sample historical data
                        for i in range(1, 6):
                            # Create records for past 5 months
                            past_month = datetime.date(
                                (today - datetime.timedelta(days=30*i)).year,
                                (today - datetime.timedelta(days=30*i)).month,
                                1
                            )
                            # Random variation in previous months' profits
                            past_profit = monthly_profit * (0.7 + (i * 0.05))
                            
                            MonthlyProfit.objects.create(
                                startup=profile,
                                date=past_month,
                                amount=past_profit
                            )
                    except Exception as profit_error:
                        # If we can't create profit records, just continue
                        # The application will use generated data instead
                        print(f"Could not create profit records: {profit_error}")
                    
                    messages.success(request, 'Profile created successfully!')
                    # Redirect to the same view to now show the profile
                    return redirect('startup:startup_profile')
                except Exception as e:
                    messages.error(request, f'Error creating profile: {str(e)}')
                    return render(request, 'startup/startup_profile.html')
            
            # If no profile exists and it's a GET request, redirect to registration
            messages.info(request, "Please complete your startup registration first.")
            return redirect('startup:startup_registration')
    except Exception as e:
        # If any database error occurs (like missing tables)
        print(f"Database error in startup_profile view: {e}")
        messages.error(request, "There was a problem with the database. Please try again later.")
        return redirect('startup:startup_registration')

@login_required
def edit_profile(request):
    # Handle database issues gracefully
    try:
        # Get the existing profile or create a new one
        profile, created = StartupProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            try:
                # Store previous monthly profit for comparison
                previous_profit = profile.monthly_profit
                
                # Update the profile with form data
                profile.startup_name = request.POST.get('startup-name', profile.startup_name)
                profile.industry = request.POST.get('industry', profile.industry)
                profile.team_size = int(request.POST.get('team_size', profile.team_size or 1))
                profile.ceo_name = request.POST.get('ceo_name', profile.ceo_name)
                profile.startup_stage = request.POST.get('startup_stage', profile.startup_stage)
                profile.equity_structure = request.POST.get('equity_structure', profile.equity_structure)
                profile.business_model = request.POST.get('business_model', profile.business_model)
                profile.company_description = request.POST.get('company_description', profile.company_description)
                profile.monthly_profit = float(request.POST.get('monthly_profit', profile.monthly_profit or 0))
                
                # Preserve contact information
                profile.website = request.POST.get('website', profile.website)
                profile.contact_email = request.POST.get('contact_email', profile.contact_email or request.user.email)
                profile.phone_number = request.POST.get('phone_number', profile.phone_number)
                profile.location = request.POST.get('location', profile.location)
                profile.country = request.POST.get('country', profile.country)
                
                print(f"Contact info saved: Website: {profile.website}, Email: {profile.contact_email}, Phone: {profile.phone_number}, Location: {profile.location}, Country: {profile.country}")
                
                # Handle profile picture upload only if a new one is provided
                if 'profile_picture' in request.FILES and request.FILES['profile_picture']:
                    profile.profile_picture = request.FILES['profile_picture']
                    
                profile.save()
                
                # Always sync with Startup model to ensure display to investors
                try:
                    startup, startup_created = Startup.objects.get_or_create(
                        user=request.user,
                        defaults={
                            'name': profile.startup_name,
                            'industry_type': profile.industry,
                            'years_in_business': 1,  # Default value
                            'annual_revenue': profile.monthly_profit * 12,
                            'profit_margin': float(request.POST.get('profit_margin', 10)),  # Get profit margin as percentage
                            'investment_required': float(request.POST.get('investment_required', 50000)),
                            'funding_purpose': profile.company_description or "Funding details not specified",
                            'target_market': request.POST.get('target_market', "Target market not specified"),
                            'growth_trend': request.POST.get('growth_trend', "stable")  # Default value
                        }
                    )
                    
                    # Update existing startup data with profile data
                    if not startup_created:
                        startup.name = profile.startup_name
                        startup.industry_type = profile.industry
                        startup.profit_margin = float(request.POST.get('profit_margin', startup.profit_margin or 10))
                        startup.annual_revenue = profile.monthly_profit * 12
                        startup.funding_purpose = profile.company_description or startup.funding_purpose
                        startup.target_market = request.POST.get('target_market', startup.target_market)
                        startup.growth_trend = request.POST.get('growth_trend', startup.growth_trend)
                        startup.investment_required = float(request.POST.get('investment_required', startup.investment_required))
                    
                    # Always sync the company logo/profile picture
                    if 'profile_picture' in request.FILES and request.FILES['profile_picture']:
                        startup.company_logo = request.FILES['profile_picture']
                    elif profile.profile_picture and not startup.company_logo:
                        # If startup has no logo but profile has picture, use that
                        startup.company_logo = profile.profile_picture
                    
                    # Handle business proposal and legal documents upload
                    if 'business_proposal' in request.FILES and request.FILES['business_proposal']:
                        startup.business_proposal = request.FILES['business_proposal']
                    
                    if 'legal_documents' in request.FILES and request.FILES['legal_documents']:
                        startup.legal_documents = request.FILES['legal_documents']
                    
                    if 'pitch_video' in request.FILES and request.FILES['pitch_video']:
                        startup.pitch_video = request.FILES['pitch_video']
                    
                    startup.save()
                    
                except Exception as startup_error:
                    print(f"Error syncing with Startup model: {startup_error}")
                
                # Update monthly profit record if profit changed
                if previous_profit != profile.monthly_profit:
                    try:
                        from accounts.models import MonthlyProfit
                        from django.utils import timezone
                        import datetime
                        
                        # Update or create current month's profit record
                        today = timezone.now().date()
                        current_month = datetime.date(today.year, today.month, 1)
                        
                        # Check if entry exists for current month
                        existing_profit = MonthlyProfit.objects.filter(
                            startup=profile,
                            date=current_month
                        ).first()
                        
                        if existing_profit:
                            existing_profit.amount = profile.monthly_profit
                            existing_profit.save()
                        else:
                            # Create new entry
                            MonthlyProfit.objects.create(
                                startup=profile,
                                date=current_month,
                                amount=profile.monthly_profit
                            )
                            
                            # If this is the first entry, create some historical data
                            if MonthlyProfit.objects.filter(startup=profile).count() <= 1:
                                # Create sample historical data for past 5 months
                                for i in range(1, 6):
                                    past_month = datetime.date(
                                        (today - datetime.timedelta(days=30*i)).year,
                                        (today - datetime.timedelta(days=30*i)).month,
                                        1
                                    )
                                    # Random variation in previous months' profits
                                    past_profit = profile.monthly_profit * (0.7 + (i * 0.05))
                                    
                                    MonthlyProfit.objects.create(
                                        startup=profile,
                                        date=past_month,
                                        amount=past_profit
                                    )
                        
                    except Exception as profit_error:
                        # If we can't update profit records, just continue
                        print(f"Could not update profit records: {profit_error}")
                
                messages.success(request, 'Profile updated successfully!')
                return redirect('startup:startup_profile')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
                return render(request, 'startup/startup_profile.html', {'profile': profile})
        
        # For GET request, get associated startup for documents
        try:
            startup = Startup.objects.get(user=request.user)
            has_startup = True
        except Startup.DoesNotExist:
            startup = None
            has_startup = False
        
        # Debug print for contact info being loaded
        print(f"Contact info loaded: Website: {profile.website}, Email: {profile.contact_email}, Phone: {profile.phone_number}, Location: {profile.location}, Country: {profile.country}")
        
        # Get profit entries for the startup profile
        try:
            from accounts.models import MonthlyProfit
            profit_entries = MonthlyProfit.objects.filter(startup=profile).order_by('-date')
            
            # Get profit data for chart
            profit_data = profile.get_monthly_profits(months=12)
        except Exception as e:
            print(f"Error getting profit data: {e}")
            profit_entries = []
            profit_data = {'labels': [], 'values': []}
        
        # Pass the profile and startup to the template for editing
        return render(request, 'startup/startup_profile.html', {
            'profile': profile,
            'startup': startup,
            'has_startup': has_startup,
            'profit_entries': profit_entries,
            'profit_data': profit_data
        })
    except Exception as e:
        # If the table doesn't exist or another error occurs
        print(f"Database error in edit_profile: {e}")
        messages.error(request, "There was an error accessing your profile. Please try again later.")
        return redirect('startup:startup_dashboard')

def startup_pro(request):
    return render(request, 'startup/startup_profile.html')

def startup_find_investors(request):
    return render(request, 'startup/find_investors.html')   

@login_required
def startup_upload_pitch(request):
    try:
        # Get the startup associated with this user
        startup = Startup.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Handle pitch video upload
            if 'pitch_video' in request.FILES:
                pitch_video = request.FILES['pitch_video']
                startup.pitch_video = pitch_video
                startup.save()
                
                # Ensure the startup profile exists and sync data
                try:
                    profile, created = StartupProfile.objects.get_or_create(
                        user=request.user,
                        defaults={
                            'startup_name': startup.name,
                            'industry': startup.industry_type,
                            'monthly_profit': startup.annual_revenue / 12 if startup.annual_revenue else 0,
                            'company_description': startup.funding_purpose
                        }
                    )
                    
                    # Update profile with startup data if created
                    if created:
                        profile.monthly_profit = startup.annual_revenue / 12 if startup.annual_revenue else 0
                        profile.startup_name = startup.name
                        profile.industry = startup.industry_type
                        profile.save()
                    
                    # If the profile doesn't have a picture but the startup has a logo, use that
                    if not profile.profile_picture and startup.company_logo:
                        profile.profile_picture = startup.company_logo
                        profile.save()
                    # If the startup doesn't have a logo but the profile has a picture, use that
                    elif not startup.company_logo and profile.profile_picture:
                        startup.company_logo = profile.profile_picture
                        startup.save()
                        
                except Exception as e:
                    print(f"Error updating startup profile: {e}")
                
                messages.success(request, "Pitch video uploaded successfully!")
                return redirect('startup:startup_dashboard')
            else:
                messages.error(request, "No video file was uploaded.")
                
        return render(request, 'startup/upload_pitch.html', {'startup': startup})
    except Startup.DoesNotExist:
        messages.warning(request, "You need to register your startup first.")
        return redirect('startup:startup_registration')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('startup:startup_dashboard')

@login_required
def find_investors(request):
    try:
        # First check if the user has a complete startup record
        if not Startup.objects.filter(user=request.user).exists():
            messages.warning(request, "You need to register your startup before viewing investors.")
            return redirect('startup:startup_registration')
            
        # Then check if they have a complete profile
        if not StartupProfile.objects.filter(user=request.user).exists():
            messages.warning(request, "Please complete your startup profile first.")
            return redirect('startup:startup_profile')
            
        # Get all users who are investors and have profiles
        investor_profiles = InvestorProfile.objects.select_related('user').all()
        
        # Get filter parameters
        investor_type = request.GET.get('investor_type')
        investment_range = request.GET.get('investment_range')
        location = request.GET.get('location')
        
        # Apply filters if they are provided
        if investor_type:
            investor_profiles = investor_profiles.filter(investor_type=investor_type)
        if investment_range:
            investor_profiles = investor_profiles.filter(investment_range=investment_range)
        if location:
            investor_profiles = investor_profiles.filter(location__icontains=location)
        
        context = {
            'investors': investor_profiles,
            'current_filters': {
                'investor_type': investor_type,
                'investment_range': investment_range,
                'location': location,
            }
        }
        return render(request, 'startup/find_investors.html', context)
    except Exception as e:
        # Log the error
        print(f"Error in find_investors: {e}")
        # Create empty context with error message
        context = {
            'investors': [],
            'error_message': "Unable to retrieve investors. Please try again later.",
        }
        messages.error(request, "There was an error retrieving investors. Please try again later.")
        return render(request, 'startup/find_investors.html', context)

@login_required
def connect_with_investor(request, investor_id):
    if request.method == 'POST':
        try:
            # Check if user has a complete startup profile
            if not StartupProfile.objects.filter(user=request.user).exists():
                messages.error(request, "You need to complete your startup profile before connecting with investors.")
                return redirect('startup:startup_profile')
                
            # Get the investor profile
            investor = get_object_or_404(InvestorProfile, id=investor_id)
            
            # Check if the user has a startup record
            if not Startup.objects.filter(user=request.user).exists():
                messages.error(request, "You need to register your startup before connecting with investors.")
                return redirect('startup:startup_registration')
                
            # Get the startup for the current user
            startup = Startup.objects.get(user=request.user)
            
            # In a real application, you would create a Connection object
            # Here we'll just show a success message
            investor_name = investor.user.get_full_name() or investor.user.username
            messages.success(request, f'Connection request sent to {investor_name}')
            
            # If you want to implement actual connection functionality:
            # 1. Create a Connection model with fields like startup, investor, status, etc.
            # 2. Create the connection record:
            # Connection.objects.create(
            #     startup=startup,
            #     investor=investor,
            #     status='pending'
            # )
            
            # 3. Optionally, send an email notification
            # from django.core.mail import send_mail
            # send_mail(
            #     f'New Connection Request from {startup.name}',
            #     f'A startup named {startup.name} wants to connect with you. Login to your dashboard to view details.',
            #     'from@example.com',
            #     [investor.user.email],
            #     fail_silently=False,
            # )
            
        except InvestorProfile.DoesNotExist:
            messages.error(request, 'Investor not found.')
        except Exception as e:
            print(f"Error in connect_with_investor: {e}")
            messages.error(request, f'An error occurred: {str(e)}')
    
    return redirect('startup:find_investors')

@login_required
def create_offer(request, startup_id):
    # Check if user is an investor
    if request.user.user_type != 'investor':
        messages.error(request, "Only investors can make offers.")
        return redirect('home')
    
    startup = get_object_or_404(Startup, id=startup_id)
    
    if request.method == 'POST':
        try:
            # Get or create investor profile for the user
            investor_profile, created = InvestorProfile.objects.get_or_create(
                user=request.user,
                defaults={
                    'investor_type': 'Individual',
                    'investment_range': '0-50000',
                }
            )
            
            equity_percentage = request.POST.get('equity_percentage')
            royalty_percentage = request.POST.get('royalty_percentage')

            # Validate percentages
            if not (0 <= float(equity_percentage) <= 100):
                messages.error(request, 'Equity percentage must be between 0 and 100.')
                return redirect('startup:create_offer', startup_id=startup.id)
            if not (0 <= float(royalty_percentage) <= 100):
                messages.error(request, 'Royalty percentage must be between 0 and 100.')
                return redirect('startup:create_offer', startup_id=startup.id)

            offer = Offer.objects.create(
                investor=investor_profile,
                startup=startup,
                equity_percentage=equity_percentage,
                royalty_percentage=royalty_percentage,
            )

            messages.success(request, 'Offer sent successfully!')
            # Redirect to a relevant page, e.g., the startup discovery page or investor dashboard
            return redirect('investor:investor_dashboard') 
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('startup:create_offer', startup_id=startup.id)

    # GET request - Render the form
    return render(request, 'investor/create_offer.html', {'startup': startup})

@login_required
def respond_to_offer(request, offer_id, response):
    offer = get_object_or_404(Offer, id=offer_id, startup__user=request.user)

    if offer.status != 'pending':
        messages.warning(request, "This offer has already been responded to.")
        return redirect('startup:manage_offers')

    if response == 'accept':
        offer.status = 'accepted'
        messages.success(request, f'Offer from {offer.investor.user.get_full_name()} accepted!')
    elif response == 'reject':
        offer.status = 'rejected'
        messages.info(request, f'Offer from {offer.investor.user.get_full_name()} rejected.')
    else:
        messages.error(request, "Invalid response.")
        return redirect('startup:manage_offers')

    offer.save()
    # Redirect back to the manage offers page
    return redirect('startup:manage_offers')

@login_required
def manage_offers(request):
    try:
        # First, check if the user is a startup user type
        if request.user.user_type.lower() != 'startup':
            messages.warning(request, "This page is only for startup users.")
            return redirect('home')
            
        # Check if the startup is registered first
        if not Startup.objects.filter(user=request.user).exists():
            messages.warning(request, "You need to register your startup before managing offers.")
            return redirect('startup:startup_registration')
            
        # Check if they have a profile
        if not StartupProfile.objects.filter(user=request.user).exists():
            messages.warning(request, "Please complete your startup profile first.")
            return redirect('startup:startup_profile')
        
        # Find startups associated with this user
        startup = Startup.objects.get(user=request.user)
        startup_profile = StartupProfile.objects.get(user=request.user)
        
        # Get all offers for this startup with related investor data
        offers = Offer.objects.filter(startup=startup).select_related('investor', 'investor__user').order_by('-created_at')
        
        # Enhanced context with detailed information
        context = {
            'offers': offers,
            'startup': startup,
            'profile': startup_profile,
            'offer_stats': {
                'total': offers.count(),
                'pending': offers.filter(status='pending').count(),
                'accepted': offers.filter(status='accepted').count(),
                'rejected': offers.filter(status='rejected').count(),
            }
        }
        return render(request, 'startup/manage_offers.html', context)
    except Exception as e:
        messages.error(request, "There was an error retrieving your offers. Please try again later.")
        return redirect('startup:startup_dashboard')

@login_required
def find_startups(request):
    # Check if user is an investor
    if request.user.user_type.lower() != 'investor':
        messages.warning(request, "This page is only for investors.")
        return redirect('home')

    # Redirect to the consolidated view in the investor app
    return redirect('investor:startup_discovery')

@login_required
@require_POST
def add_profit_entry(request):
    try:
        data = json.loads(request.body)
        
        # Get startup profile associated with user
        try:
            startup_profile = StartupProfile.objects.get(user=request.user)
        except StartupProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'No startup profile found for this user'}, status=400)
        
        # Extract and validate profit data
        date_str = data.get('date')
        amount = data.get('amount')
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid date format'}, status=400)
        
        try:
            amount = float(amount)
            if amount < 0:
                return JsonResponse({'success': False, 'error': 'Amount cannot be negative'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid amount'}, status=400)
        
        # Create or update profit entry
        profit_entry, created = MonthlyProfit.objects.update_or_create(
            startup=startup_profile,
            date=date,
            defaults={'amount': amount}
        )
        
        return JsonResponse({
            'success': True, 
            'created': created,
            'profit_id': profit_entry.id,
            'date': date_str,
            'amount': amount
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def delete_profit_entry(request):
    try:
        data = json.loads(request.body)
        profit_id = data.get('profit_id')
        
        try:
            profit = MonthlyProfit.objects.get(id=profit_id)
        except MonthlyProfit.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profit entry not found'}, status=404)
        
        # Security check - ensure user owns this startup profile
        if profit.startup.user != request.user:
            return JsonResponse({'success': False, 'error': 'Unauthorized access'}, status=403)
        
        # Delete the profit entry
        profit.delete()
        
        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)