from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Startup
from accounts.models import InvestorProfile, CustomUser

@login_required
def startup_registration(request):
    if request.method == 'POST':
        try:
            # Create new startup record with correct field names
            startup = Startup(
                # Basic Details (match these to your model fields)
                name=request.POST.get('startup-name'),  # Changed from startup_name to name
                industry_type=request.POST.get('industry-type'),
                years_in_business=request.POST.get('years-in-business'),
                company_logo=request.FILES.get('company-logo'),
                
                # Financial Info
                annual_revenue=request.POST.get('revenue'),  # Changed from revenue to annual_revenue
                profit_margin=request.POST.get('profit-margin'),
                investment_required=request.POST.get('investment-required'),
                funding_purpose=request.POST.get('funding-purpose'),
                
                # Market Insights
                target_market=request.POST.get('target-market'),
                growth_trend=request.POST.get('growth-trend'),
                pitch_video=request.FILES.get('pitch-video'),
                
                # Supporting Docs
                business_proposal=request.FILES.get('business-proposal'),
                legal_documents=request.FILES.get('legal-documents')
            )
            startup.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Startup registered successfully!',
                    'redirect_url': '/startup/dashboard/'
                })
            else:
                messages.success(request, 'Startup registered successfully!')
                return redirect('startup_dashboard')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                }, status=400)
            else:
                messages.error(request, str(e))
                return redirect('startup_registration')
    
    # GET request - show the form
    return render(request, 'forms.html')


def startup_dashboard(request):
    return render(request, 'startup/startup_dashboard.html')

def startup_insights(request):
    return render(request, 'startup/startup_insights.html')

def startup_pro(request):
    return render(request, 'startup/startup_profile.html')

def startup_find_investors(request):
    return render(request, 'startup/find_investors.html')   

def startup_upload_pitch(request):
    return render(request, 'startup/upload_pitch.html')

@login_required
def find_investors(request):
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
    return redirect('find_investors')