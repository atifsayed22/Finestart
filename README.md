# FineStart - Startup-Investor Matchmaking Platform

FineStart is a web application designed to connect startups with potential investors. It provides a platform for startups to showcase their business profiles and for investors to discover promising ventures.

## Project Structure

The application is divided into three main Django apps:

1. **Accounts**: Handles user authentication, registration, and profile management
2. **Startup**: Contains functionality specific to startup users
3. **Investor**: Contains functionality specific to investor users

## Features

- Dual user types (Startup and Investor)
- Comprehensive user profiles
- Startup financial tracking
- Investor portfolio management
- Investment offer system
- Startup discovery for investors
- Investor discovery for startups
- Insights and analytics

## Implementation Details

### Accounts App

#### Models

- **CustomUser**: Extends Django's AbstractUser with additional fields:
  - `user_type`: Distinguishes between 'startup' and 'investor' users
  - `is_verified`: Indicates if the user has verified their account

- **StartupProfile**: Stores detailed information about a startup:
  - Basic information (name, industry, team size, etc.)
  - Financial details (monthly profit)
  - Business model and equity structure
  - Contact information (website, email, phone, location)
  - Profile picture

- **MonthlyProfit**: Tracks a startup's profit over time:
  - Associated with a StartupProfile
  - Contains date and amount fields
  - Used for generating profit trend charts

- **InvestorProfile**: Stores detailed information about an investor:
  - Investment preferences (type, range)
  - Company details (if applicable)
  - Portfolio size
  - Contact information

#### Views

- **Authentication Views**: Login, logout, and registration functionality
  - Different redirection based on user type
  - Custom forms for startup and investor registration

- **Profile Management Views**: Create and update user profiles
  - Separate workflows for startup and investor profiles
  - File upload handling for profile pictures and documents

### Startup App

#### Models

- **Startup**: Contains business details beyond profile information:
  - Financial metrics (annual revenue, profit margin)
  - Investment requirements
  - Business documentation (proposals, legal docs)
  - Growth trends

- **Offer**: Represents investment offers:
  - Associated with a startup and investor
  - Includes details like equity percentage and royalty percentage
  - Tracks offer status (pending, accepted, rejected)

#### Views

1. **startup_registration** (`/startup/register/`)
   - Handles startup registration with detailed business information
   - Processes form submissions with file uploads
   - Creates both Startup and StartupProfile records
   - Implements AJAX support for dynamic form submission
   - Error handling for missing or invalid fields

2. **startup_dashboard** (`/startup/dashboard/`)
   - Entry point for startup users after login
   - Displays summary of startup metrics and pending offers
   - Shows profit/loss chart using Chart.js
   - Provides navigation to other startup features
   - Handles cases for incomplete profiles or missing startup registration

3. **startup_profile** (`/startup/profile/`)
   - Displays the startup's complete profile
   - Shows profit trend chart using monthly profit data
   - Links to profile editing functionality

4. **edit_profile** (`/startup/profile/edit/`)
   - Form for updating startup profile information
   - Handles file uploads (profile picture, documents)
   - Updates associated Startup record for data consistency
   - Monthly profit tracking with historical data

5. **profit_data** (`/startup/profit_data/`)
   - AJAX endpoint for fetching profit history
   - Returns JSON for chart rendering

6. **add_profit_entry** (`/startup/add_profit_entry/`)
   - AJAX endpoint for adding a new monthly profit entry
   - Validates date and amount data
   - Creates or updates MonthlyProfit records

7. **delete_profit_entry** (`/startup/delete_profit_entry/`)
   - AJAX endpoint for removing profit entries
   - Security verification to ensure user owns the entry

8. **startup_insights** (`/startup/insights/`)
   - Provides analytics and scoring for the startup
   - Calculates various performance metrics:
     - Information quality score
     - Financial score
     - Maturity score
     - Team score
     - Market score
   - Performs risk assessment for investors
   - Displays profit trend visualization

9. **find_investors** (`/startup/find_investors/`)
   - Lists available investors with filtering options
   - Filters by investor type, investment range, and location
   - Displays investor cards with relevant information
   - Includes form for contacting/connecting with investors

10. **connect_with_investor** (`/startup/connect_with_investor/<investor_id>/`)
    - Handles connection requests to investors
    - Validates startup profile completeness
    - Success/error messaging system

11. **manage_offers** (`/startup/manage_offers/`)
    - Lists all offers received by the startup
    - Groups offers by status (pending, accepted, rejected)
    - Provides interface to respond to pending offers
    - Displays offer statistics

12. **respond_to_offer** (`/startup/respond_to_offer/<offer_id>/<response>/`)
    - Processes startup responses to investment offers
    - Updates offer status based on response (accept/reject)
    - Redirects back to offer management view

13. **startup_upload_pitch** (`/startup/upload_pitch/`)
    - Specialized view for uploading and managing pitch videos
    - Updates both Startup and StartupProfile records
    - Handles file validation and storage

### Investor App

#### Views

1. **investor_dashboard** (`/investor/dashboard/`)
   - Main dashboard for investor users
   - Displays portfolio summary and investment statistics
   - Shows pending and recent offers
   - Provides navigation to investor features

2. **investor_profile** (`/investor/profile/`)
   - Displays and manages investor profile information
   - Handles profile picture and company logo uploads
   - Updates preferences and investment criteria

3. **startup_discovery** (`/investor/discover/`)
   - Lists startups matching investor criteria
   - Advanced filtering by industry, growth stage, etc.
   - Sorted view of potential investment opportunities
   - Interface for viewing detailed startup information

4. **portfolio_tracker** (`/investor/portfolio/`)
   - Tracks current investments and their performance
   - Visualizes portfolio distribution
   - Monitors return on investment metrics

5. **create_offer** (`/startup/create_offer/<startup_id>/`)
   - Form for creating investment offers
   - Validates equity and royalty percentages
   - Associates offer with the investor and target startup

6. **find_startups** (`/investor/find_startups/`)
   - Search interface for discovering startups
   - Filters startups by various criteria
   - Displays startup cards with key metrics

## Routing

### Accounts App URLs

```python
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    # Profile routes handled by respective apps
]
```

### Startup App URLs

```python
app_name = 'startup'

urlpatterns = [
    path('register/', views.startup_registration, name='startup_registration'),
    path('dashboard/', views.startup_dashboard, name='startup_dashboard'),
    path('insights/', views.startup_insights, name='startup_insights'),
    path('profile/', views.startup_profile, name='startup_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('find_investors/', views.find_investors, name='find_investors'),
    path('connect_with_investor/<int:investor_id>/', views.connect_with_investor, 
        name='connect_with_investor'),
    path('upload_pitch/', views.startup_upload_pitch, name='startup_upload_pitch'),
    path('manage_offers/', views.manage_offers, name='manage_offers'),
    path('create_offer/<int:startup_id>/', views.create_offer, name='create_offer'),
    path('respond_to_offer/<int:offer_id>/<str:response>/', views.respond_to_offer, 
        name='respond_to_offer'),
    path('find_startups/', views.find_startups, name='find_startups'),
    path('add_profit_entry/', views.add_profit_entry, name='add_profit_entry'),
    path('delete_profit_entry/', views.delete_profit_entry, name='delete_profit_entry'),
    path('profit_data/', views.profit_data, name='profit_data'),
]
```

### Investor App URLs

```python
app_name = 'investor'

urlpatterns = [
    path('dashboard/', views.investor_dashboard, name='investor_dashboard'),
    path('profile/', views.investor_profile, name='investor_profile'),
    path('discover/', views.startup_discovery, name='startup_discovery'),
    path('portfolio/', views.portfolio_tracker, name='portfolio_tracker'),
    # Additional investor-specific routes
]
```

## Templates Structure

Each app has its own templates directory following this structure:

```
templates/
├── accounts/
│   ├── login.html
│   └── signup.html
├── startup/
│   ├── startup_dashboard.html
│   ├── startup_profile.html
│   ├── find_investors.html
│   ├── manage_offers.html
│   └── ...
└── investor/
    ├── investor_dashboard.html
    ├── investor_profile.html
    ├── startup_discovery.html
    └── ...
```

## Authentication Flow

1. User registers selecting their user type (startup/investor)
2. Upon login, users are redirected based on their type:
   - Startup users to `/startup/dashboard/`
   - Investor users to `/investor/dashboard/`
3. New users are prompted to complete their profiles

## Data Flow for Investment Process

1. Investor discovers startups via `/investor/discover/`
2. Investor creates an offer via `/startup/create_offer/<startup_id>/`
3. Startup receives offer notification on their dashboard
4. Startup reviews and manages offers via `/startup/manage_offers/`
5. Startup accepts or rejects offer via `/startup/respond_to_offer/<offer_id>/<response>/`
6. If accepted, offer appears in investor's portfolio

## Technical Implementation Notes

- Django template system with extensive use of template inheritance
- AJAX for dynamic data updates (profit entries, filtering)
- Form validation on both client and server side
- Security measures to ensure users can only access their own data
- File upload handling for various document types
- Chart.js for data visualization

## Installation and Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver` 

## Startup Scoring System

The platform uses a comprehensive scoring system (0-100) to evaluate startups and provide investors with objective metrics. The total score is calculated based on several component scores:

### Score Components

1. **Information Quality Score (20% of total)**
   - Quality of company description (up to 10 points)
   - Profile picture/logo presence (5 points)
   - Pitch video availability (5 points)

2. **Financial Score (30% of total)**
   - Annual revenue (up to 15 points)
     - Scaled based on revenue amount, with a maximum at $100,000+
   - Profit margin (up to 15 points)
     - Scaled as a percentage, with maximum points at 100% margin

3. **Maturity Score (25% of total)**
   - Years in business (up to 15 points)
     - 3 points per year, capped at 5 years
   - Business model clarity (5 points)
   - Equity structure documentation (5 points)

4. **Team Score (10% of total)**
   - Team size (up to 10 points)
     - 1 point per team member, capped at 10 members

5. **Market Score (15% of total)**
   - Target market clarity (5 points)
   - Growth trend (up to 10 points)
     - Rapid growth: 10 points
     - Steady growth: 5 points
     - Declining: 0 points

### Score Calculation Formula

```python
def calculate_startup_score(startup, profile):
    # Component scores
    info_score = calculate_info_score(startup, profile)
    financial_score = calculate_financial_score(startup, profile)
    maturity_score = calculate_maturity_score(startup, profile)
    team_score = calculate_team_score(profile)
    market_score = calculate_market_score(startup, profile)
    
    # Total score (capped at 100)
    total_score = info_score + financial_score + maturity_score + team_score + market_score
    return min(100, int(total_score))
```

## Risk Assessment System

The platform also performs a risk assessment for each startup, categorizing them as Low, Medium, or High risk based on various risk factors:

### Risk Factors

1. **Financial Risk**
   - Annual revenue < $10,000: +2 risk points
   - Annual revenue < $50,000: +1 risk point
   - Negative profit margin: +2 risk points
   - Profit margin < 10%: +1 risk point

2. **Business Maturity Risk**
   - Less than 1 year in business: +2 risk points
   - Less than 3 years in business: +1 risk point

3. **Market Risk**
   - Declining growth trend: +2 risk points
   - Stable growth trend: +1 risk point
   - Rapid growth trend: 0 risk points

4. **Team Risk**
   - Team size < 3 members: +1 risk point

### Risk Assessment Formula

```python
def assess_startup_risk(startup, profile):
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
```

This scoring and risk assessment system helps investors make informed decisions by providing standardized metrics while allowing startups to understand areas they can improve to attract more investment. 

## File and Image Upload Management

The platform handles various types of file uploads throughout the application, including profile pictures, company logos, pitch videos, and business documents. Here's how these uploads are managed:

### Storage Configuration

Files are stored using Django's FileField and ImageField, configured with the following settings:

```python
# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Files are organized in subdirectories based on their type:
- Profile pictures: `media/profiles/`
- Company logos: `media/logos/`
- Pitch videos: `media/videos/`
- Business documents: `media/documents/`
- Legal documents: `media/documents/`

### Pillow Integration for Image Processing

The platform uses Pillow (PIL Fork) for advanced image processing tasks. Pillow is a powerful Python imaging library that extends the capabilities of Django's ImageField.

#### Installation and Configuration

Pillow is included in the project dependencies:
```
# requirements.txt
Pillow==9.5.0
```

Django settings are configured to work with Pillow:
```python
INSTALLED_APPS = [
    # ...
    'django.contrib.staticfiles',
    'accounts',
    'startup',
    'investor',
    # ...
]

# Pillow-related settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
```

#### Image Processing Functions

1. **Image Resizing and Thumbnail Generation**

```python
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def resize_image(image_field, max_size=(300, 300)):
    """Resize an image to fit within the specified dimensions."""
    if not image_field:
        return None
        
    img = Image.open(image_field)
    
    # Convert to RGB if image has transparency (for JPEG output)
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
        img = bg
    
    # Calculate aspect ratio and resize
    img.thumbnail(max_size, Image.LANCZOS)
    
    # Save to in-memory file
    output = BytesIO()
    img.save(output, format='JPEG', quality=85)
    output.seek(0)
    
    # Create a new Django-friendly UploadedFile
    return InMemoryUploadedFile(
        output,
        'ImageField',
        f"{image_field.name.split('.')[0]}.jpg",
        'image/jpeg',
        sys.getsizeof(output),
        None
    )
```

2. **Profile Picture Processing**

This function is called in the `save` method of the `StartupProfile` and `InvestorProfile` models:

```python
def save(self, *args, **kwargs):
    # Process profile picture on save
    if self.profile_picture:
        # Check if this is a new image (not yet processed)
        if not self._state.adding and self.__class__.objects.get(pk=self.pk).profile_picture != self.profile_picture:
            self.profile_picture = resize_image(self.profile_picture, (300, 300))
            
    super().save(*args, **kwargs)
```

3. **Logo Processing for Startups**

```python
def process_company_logo(instance, filename):
    """Process company logo before saving."""
    img = Image.open(instance.company_logo)
    
    # Create a square image with white background
    size = max(img.size)
    new_img = Image.new('RGB', (size, size), (255, 255, 255))
    
    # Paste original image centered
    position = ((size - img.width) // 2, (size - img.height) // 2)
    new_img.paste(img, position)
    
    # Resize to standard size
    new_img.thumbnail((400, 400), Image.LANCZOS)
    
    # Save to memory
    output = BytesIO()
    new_img.save(output, format='PNG', quality=90)
    output.seek(0)
    
    # Return processed image
    return InMemoryUploadedFile(
        output,
        'ImageField',
        f"{filename.split('.')[0]}.png",
        'image/png',
        sys.getsizeof(output),
        None
    )
```

#### Image Optimization

For production environments, the platform implements additional image optimization:

```python
def optimize_image(image_path):
    """Further optimize images for web delivery."""
    img = Image.open(image_path)
    
    # Apply web optimization
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Apply slight sharpening filter
    from PIL import ImageEnhance
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.1)
    
    # Save with optimized settings
    img.save(image_path, 'JPEG', quality=85, optimize=True, progressive=True)
```

#### Advanced Features

1. **Watermarking for Premium Startups**

Premium startups have their logos watermarked with a subtle branding element:

```python
def add_watermark(image, watermark_text="Premium"):
    """Add a subtle watermark to premium startup logos."""
    img = Image.open(image)
    drawing = ImageDraw.Draw(img)
    
    # Load a font
    font = ImageFont.truetype("arial.ttf", 15)
    
    # Position text at bottom right
    position = (img.width - 80, img.height - 20)
    
    # Draw semi-transparent text
    drawing.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)
    
    # Save to memory
    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    
    return InMemoryUploadedFile(
        output,
        'ImageField',
        image.name,
        'image/png',
        sys.getsizeof(output),
        None
    )
```

2. **Image Analysis for Content Moderation**

Basic image analysis is performed to detect inappropriate content:

```python
def validate_image_content(image):
    """Perform basic image analysis to detect inappropriate content."""
    img = Image.open(image)
    
    # Basic skin tone detection (simplified)
    from PIL import ImageStat
    stat = ImageStat.Stat(img)
    r, g, b = stat.mean
    
    # Simplified inappropriate content detection
    if r > 2*g and r > 2*b and r > 200:
        return False, "Image may contain inappropriate content"
    
    return True, "Image passed validation"
```

### Implementation in Views

Pillow functionality is integrated into views that handle file uploads:

```python
@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        try:
            # Get profile based on user type
            if request.user.user_type == 'startup':
                profile = StartupProfile.objects.get(user=request.user)
            else:
                profile = InvestorProfile.objects.get(user=request.user)
            
            # Process the image with Pillow
            original_image = request.FILES['profile_picture']
            processed_image = resize_image(original_image)
            
            # Update profile
            profile.profile_picture = processed_image
            profile.save()
            
            messages.success(request, "Profile picture updated successfully!")
            return redirect('profile')
            
        except Exception as e:
            messages.error(request, f"Error updating profile picture: {str(e)}")
    
    return redirect('profile')
```

This comprehensive image processing system ensures consistent image quality across the platform while maintaining performance and security standards. 