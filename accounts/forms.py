from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StartupProfile, InvestorProfile

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPES, widget=forms.RadioSelect)
    
    
    # Additional fields for startup
    startup_name = forms.CharField(max_length=255, required=False)
    industry = forms.CharField(max_length=100, required=False)
    
    # Additional fields for investor
    investor_type = forms.CharField(max_length=100, required=False)
    investment_range = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        user.is_verified = False
        
        if commit:
            user.save()
            
            # Create profile based on user type with error handling
            try:
                if user.user_type == 'startup':
                    StartupProfile.objects.create(
                        user=user,
                        startup_name=self.cleaned_data.get('startup_name', ''),
                        industry=self.cleaned_data.get('industry', '')
                    )
                elif user.user_type == 'investor':
                    InvestorProfile.objects.create(
                        user=user,
                        investor_type=self.cleaned_data.get('investor_type', ''),
                        investment_range=self.cleaned_data.get('investment_range', '')
                    )
            except Exception as e:
                # Log error but don't raise it - user is still created
                print(f"Error creating profile during signup: {e}")
                
        return user
