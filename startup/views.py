from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Startup

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
            
            return JsonResponse({
                'success': True,
                'message': 'Startup registered successfully!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    # GET request - show the form
    return render(request, 'forms.html')


def startup_dashboard(request):
    return render(request, 'startup/startup_dashboard.html')

def startup_insights(request):
    return render(request, 'startup/startup_insights.html')

def startup_profile(request):
    return render(request, 'startup/startup_profile.html')

def startup_find_investors(request):
    return render(request, 'startup/startup_find_investors.html')   

def startup_upload_pitch(request):
    return render(request, 'startup/upload_pitch.html')

def find_investors(request):
    return render(request, 'startup/find_investors.html')