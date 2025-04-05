from django import forms

class BasicDetailsForm(forms.Form):
    startup_name = forms.CharField(
        label="Startup Name",
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your startup name',
            'class': 'form-control'
        })
    )
    
    industry_type = forms.ChoiceField(
        label="Industry Type",
        choices=[('tech', 'Technology'), ('fintech', 'Fintech'), ('healthcare', 'Healthcare'), ('education', 'Education'), ('other', 'Other')],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    years_in_business = forms.IntegerField(
        label="Years in Business",
        min_value=0,
        max_value=50,
        required=True,
        widget=forms.NumberInput(attrs={
            'placeholder': '0-50',
            'class': 'form-control'
        })
    )
    
    company_logo = forms.ImageField(
        label="Company Logo",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )


class FinancialInfoForm(forms.Form):
    revenue = forms.DecimalField(
        label="Annual Revenue ($)",
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g. 50000',
            'class': 'form-control'
        })
    )
    
    profit_margin = forms.DecimalField(
        label="Profit Margin (%)",
        min_value=0,
        max_value=100,
        decimal_places=1,
        required=True,
        widget=forms.NumberInput(attrs={
            'placeholder': '0-100%',
            'class': 'form-control'
        })
    )
    
    investment_required = forms.DecimalField(
        label="Investment Required ($)",
        min_value=0,
        required=True,
        widget=forms.NumberInput(attrs={
            'placeholder': 'e.g. 100000',
            'class': 'form-control'
        })
    )
    
    funding_purpose = forms.CharField(
        label="Funding Purpose",
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe how you will use the investment',
            'class': 'form-control',
            'rows': 4
        }),
        required=True
    )


class MarketInsightsForm(forms.Form):
    target_market = forms.CharField(
        label="Target Market Description",
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe your ideal customers',
            'class': 'form-control',
            'rows': 4
        }),
        required=True
    )
    
    growth_trend = forms.ChoiceField(
        label="Business Growth Trend",
        choices=[('growing', 'Growing'), ('stable', 'Stable'), ('declining', 'Declining')],
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    pitch_video = forms.FileField(
        label="Pitch Video",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'video/*'
        })
    )