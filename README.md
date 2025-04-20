# FineStart - Startup-Investor Matchmaking Platform

FineStart is a comprehensive platform connecting startups with potential investors, providing tools for startup profile management, investor discovery, and financial tracking.

## Startup Scoring System

The platform includes a proprietary scoring algorithm that evaluates startups on a scale of 0-100 based on various factors. This score helps investors quickly assess startup quality and helps founders understand their startup's strengths and weaknesses.

### Score Components

The scoring system evaluates 5 key areas:

1. **Company Information (20 points)**
   - Company description quality (5-10 points)
   - Profile picture presence (5 points)
   - Pitch video availability (5 points)

2. **Financial Metrics (30 points)**
   - Annual revenue (up to 15 points)
   - Profit margin (up to 15 points)

3. **Business Maturity (25 points)**
   - Years in business (up to 15 points)
   - Business model clarity (5 points)
   - Equity structure definition (5 points)

4. **Team Size (10 points)**
   - Larger teams receive higher scores (up to 10 points)

5. **Market Factors (15 points)**
   - Target market definition (5 points)
   - Growth trend (10 points for rapid growth, 5 for steady growth)

### How Scores Are Calculated

- **Annual Revenue Scoring**: 1 point for every $6,667 in revenue, up to 15 points max
- **Profit Margin Scoring**: 1 point for every 0.67% profit margin, up to 15 points max
- **Years in Business**: 3 points per year, up to 15 points max
- **Team Size**: 1 point per team member, up to 10 points max

## Risk Assessment Algorithm

The risk assessment algorithm determines whether a startup represents a Low, Medium, or High risk investment opportunity.

### Risk Factors Evaluated

The system counts risk factors in these categories:

1. **Financial Risk**
   - Annual revenue < $10,000: +2 risk factors
   - Annual revenue < $50,000: +1 risk factor
   - Profit margin ≤ 0%: +2 risk factors
   - Profit margin < 10%: +1 risk factor

2. **Business Maturity**
   - Years in business < 1: +2 risk factors
   - Years in business < 3: +1 risk factor

3. **Market Factors**
   - Declining growth trend: +2 risk factors
   - Stable growth trend: +1 risk factor

4. **Team Factors**
   - Team size < 3: +1 risk factor

### Risk Categorization

- **Low Risk**: 0-2 risk factors
- **Medium Risk**: 3-5 risk factors
- **High Risk**: 6+ risk factors

## Implementing These Features for Investors

### Displaying Startup Insights to Investors

To implement the display of startup scores and risk assessment to investors:

1. **Startup Discovery Page**:
   - Add score and risk indicators to each startup card
   - Use color-coding (green/yellow/red) for risk levels
   - Sort startups by score (default highest first)

2. **Startup Detail View**:
   - Add a "View Insights" button that shows the detailed scoring breakdown
   - Display the score prominently at the top of the detail page
   - Show risk assessment with explanatory text

3. **Filtering Options**:
   - Add filters for score ranges (e.g., 70-100, 40-70, 0-40)
   - Add filters for risk level (Low, Medium, High)
   - Allow sorting by different score components

### Technical Implementation

The scoring and risk assessment are implemented in the `startup/views.py` file with the following functions:

- `calculate_startup_score()`: Main function that calculates the overall score
- `calculate_info_score()`: Evaluates company information quality
- `calculate_financial_score()`: Evaluates financial metrics
- `calculate_maturity_score()`: Evaluates business maturity
- `calculate_team_score()`: Evaluates team size
- `calculate_market_score()`: Evaluates market factors
- `assess_startup_risk()`: Determines the risk level

These scores are displayed on the insights page (`startup/templates/startup/startup_insights.html`) with visualizations including:

- Circular progress indicator for the overall score
- Progress bars for each score component
- Color-coded risk level indicator
- Monthly profit trend chart
- Personalized recommendations based on the score

## Setup and Installation

### Requirements
- Python 3.8+
- Django 3.2+
- Chart.js for data visualization

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/finestart.git
cd finestart
```

2. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run migrations:
```
python manage.py migrate
```

5. Run the development server:
```
python manage.py runserver
``` 