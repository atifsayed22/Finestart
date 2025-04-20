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