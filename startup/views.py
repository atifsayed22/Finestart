from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Startup
from accounts.models import InvestorProfile, CustomUser, StartupProfile
import json

@login_required
def startup_registration(request):
    # First check if the user already has a profile
    try:
        if StartupProfile.objects.filter(user=request.user).exists():
            # If profile exists, redirect to the profile view
            return redirect('startup:startup_profile')
    except Exception as e:
        print(f"Error checking for existing profile: {e}")
    
    if request.method == 'POST':
        try:
            print("Registration submission received")
            # Print request data for debugging
            print(f"POST data: {request.POST}")
            print(f"FILES data: {request.FILES}")
            
            # Basic input validation to prevent errors
            name = request.POST.get('startup-name', '')
            industry_type = request.POST.get('industry-type', '')
            years_in_business = request.POST.get('years-in-business', 0)
            
            if not name:
                raise ValueError("Startup name is required")
            
            if not industry_type:
                raise ValueError("Industry type is required")
            
            # Financial validation with defaults to prevent type errors
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
            
            # Other fields with defaults
            funding_purpose = request.POST.get('funding-purpose', '')
            target_market = request.POST.get('target-market', '')
            growth_trend = request.POST.get('growth-trend', '')
            
            # Handle file uploads safely
            company_logo = request.FILES.get('company-logo') if 'company-logo' in request.FILES else None
            pitch_video = request.FILES.get('pitch-video') if 'pitch-video' in request.FILES else None
            business_proposal = request.FILES.get('business-proposal') if 'business-proposal' in request.FILES else None
            legal_documents = request.FILES.get('legal-documents') if 'legal-documents' in request.FILES else None
            
            # Create new startup record with validated data
            startup = Startup(
                # Basic Details
                name=name,
                industry_type=industry_type,
                years_in_business=years_in_business,
                company_logo=company_logo,
                
                # Financial Info
                annual_revenue=annual_revenue,
                profit_margin=profit_margin,
                investment_required=investment_required,
                funding_purpose=funding_purpose,
                
                # Market Insights
                target_market=target_market,
                growth_trend=growth_trend,
                pitch_video=pitch_video,
                
                # Supporting Docs
                business_proposal=business_proposal,
                legal_documents=legal_documents
            )
            startup.save()
            
            # Make sure we have a startup profile
            try:
                startup_profile, created = StartupProfile.objects.get_or_create(
                    user=request.user,
                    defaults={
                        'startup_name': name,
                        'industry': industry_type,
                        'monthly_profit': profit_margin
                    }
                )
            except Exception as profile_error:
                print(f"Could not create startup profile: {profile_error}")
                # Continue even if profile creation fails
            
            # Check if this is an AJAX request
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
            
            # Check if this is an AJAX request
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'message': f"Error: {error_message}"
                }, status=400)
            else:
                messages.error(request, error_message)
                return redirect('startup:startup_registration')
    
    # GET request - show the form
    return render(request, 'forms.html')


def startup_dashboard(request):
    # Pass user information to the dashboard
    context = {}
    try:
        # Check if the user has a startup profile
        profile = StartupProfile.objects.get(user=request.user)
        context['profile'] = profile
    except StartupProfile.DoesNotExist:
        # Handle the case when no profile exists
        pass
    except Exception as e:
        print(f"Error getting startup profile for dashboard: {e}")
    
    # Pass the welcome message to the template
    if request.user.is_authenticated:
        welcome_name = request.user.first_name if request.user.first_name else request.user.username
        context['welcome_name'] = welcome_name
        
    return render(request, 'startup/startup_dashboard.html', context)

def startup_insights(request):
    return render(request, 'startup/startup_insights.html')

@login_required
def startup_profile(request):
    # Handle potential database errors
    try:
        # Check if the user already has a profile
        try:
            profile = StartupProfile.objects.get(user=request.user)
            # Get profit data for the chart
            profit_data = profile.get_monthly_profits(months=6)
            # If profile exists, show the profile view
            return render(request, 'startup/profile_view.html', {
                'profile': profile,
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
                        monthly_profit=monthly_profit
                    )
                    
                    # Handle profile picture upload
                    if 'profile_picture' in request.FILES:
                        profile.profile_picture = request.FILES['profile_picture']
                        
                    profile.save()
                    
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
            
            # If no profile exists and it's a GET request, show the profile form
            return render(request, 'startup/startup_profile.html')
    except Exception as e:
        # If any database error occurs (like missing tables)
        print(f"Database error in startup_profile view: {e}")
        messages.error(request, "There was a problem with the database. Please try again later.")
        return render(request, 'startup/startup_profile.html')

@login_required
def edit_profile(request):
    # Handle database issues gracefully
    try:
        # Get the existing profile or create a new one
        profile, created = StartupProfile.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            try:
                previous_profit = profile.monthly_profit
                
                # Update the profile with form data
                profile.startup_name = request.POST.get('startup-name', profile.startup_name)
                profile.industry = request.POST.get('industry', profile.industry)
                profile.team_size = int(request.POST.get('team_size', 1))
                profile.ceo_name = request.POST.get('ceo_name', profile.ceo_name)
                profile.startup_stage = request.POST.get('startup_stage', profile.startup_stage)
                profile.equity_structure = request.POST.get('equity_structure', profile.equity_structure)
                profile.business_model = request.POST.get('business_model', profile.business_model)
                profile.company_description = request.POST.get('company_description', profile.company_description)
                profile.monthly_profit = float(request.POST.get('monthly_profit', profile.monthly_profit))
                
                # Handle profile picture upload
                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture']
                    
                profile.save()
                
                # Update monthly profit record if profit changed
                if previous_profit != profile.monthly_profit:
                    try:
                        from accounts.models import MonthlyProfit
                        from django.utils import timezone
                        import datetime
                        
                        # Update or create current month's profit record
                        today = timezone.now().date()
                        current_month = datetime.date(today.year, today.month, 1)
                        
                        MonthlyProfit.objects.update_or_create(
                            startup=profile,
                            date=current_month,
                            defaults={'amount': profile.monthly_profit}
                        )
                    except Exception as profit_error:
                        # If we can't update profit records, just continue
                        print(f"Could not update profit records: {profit_error}")
                
                messages.success(request, 'Profile updated successfully!')
                return redirect('startup:startup_profile')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
                return render(request, 'startup/startup_profile.html', {'profile': profile})
        
        # Pass the profile to the template for editing
        return render(request, 'startup/startup_profile.html', {'profile': profile})
    except Exception as e:
        # If the table doesn't exist or another error occurs
        print(f"Database error in edit_profile: {e}")
        messages.error(request, "There was an error accessing your profile. Please try again later.")
        return redirect('startup:startup_dashboard')

def startup_pro(request):
    return render(request, 'startup/startup_profile.html')

def startup_find_investors(request):
    return render(request, 'startup/find_investors.html')   

def startup_upload_pitch(request):
    return render(request, 'startup/upload_pitch.html')

@login_required
def find_investors(request):
    try:
        # Get all users who are investors and have profiles
        investors = InvestorProfile.objects.select_related('user').all()
        
        # Get filter parameters
        industry = request.GET.get('industry')
        region = request.GET.get('region')
        funding_stage = request.GET.get('funding_stage')
        investment_range = request.GET.get('investment_range')
        
        # Apply filters if they are provided
        if industry:
            investors = investors.filter(user__startupprofile__industry=industry)
        if investment_range:
            investors = investors.filter(investment_range=investment_range)
        
        context = {
            'investors': investors,
            'current_filters': {
                'industry': industry,
                'region': region,
                'funding_stage': funding_stage,
                'investment_range': investment_range,
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
            'current_filters': {
                'industry': None,
                'region': None,
                'funding_stage': None,
                'investment_range': None,
            }
        }
        messages.error(request, "There was an error retrieving investors. Please try again later.")
        return render(request, 'startup/find_investors.html', context)

@login_required
def connect_with_investor(request, investor_id):
    if request.method == 'POST':
        try:
            investor = InvestorProfile.objects.get(id=investor_id)
            # Here you would typically create a connection/message record
            # For now, we'll just show a success message
            messages.success(request, f'Connection request sent to {investor.user.get_full_name()}')
        except InvestorProfile.DoesNotExist:
            messages.error(request, 'Investor not found.')
    return redirect('startup:find_investors')