# Net Worth Tracker

A comprehensive personal finance management application that helps you track your net worth, manage accounts, and monitor your financial progress over time with advanced analytics.

## 🚀 Features

### Core Functionality
- **Net Worth Tracking:** Monitor your total net worth with monthly snapshots
- **Account Management:** Track multiple account types (checking, savings, investments, loans, etc.)
- **Transaction Tracking:** Record income, expenses, and transfers
- **Advanced Analytics:** Comprehensive financial insights and visualizations
- **Data Export:** Export your data in CSV, Excel, and PDF formats
- **Multi-Currency Support:** Track accounts in different currencies
- **Asset Classification:** Categorize assets by type (cash, crypto, property, etc.)

### Analytics Features
- **Net Worth Trends:** Track your net worth over time with interactive charts
- **Asset Allocation:** Visual breakdown of your asset distribution
- **Income vs Expenses:** Monthly comparison of income and spending
- **Spending Analysis:** Category-based spending breakdown
- **Account Performance:** Individual account growth tracking
- **Financial Ratios:** Key financial health indicators
- **Savings Rate:** Calculate and track your savings percentage
- **Emergency Fund Ratio:** Monitor your emergency fund adequacy

## 🏗️ Project Structure

```
networthtracker/
├── backend/           # Django project configuration
│   ├── settings.py    # Django settings
│   ├── urls.py        # Main URL configuration
│   └── wsgi.py        # WSGI configuration
├── dashboard/         # Main dashboard app
│   ├── models.py      # Data models (Account, Transaction, AccountEntry)
│   ├── views.py       # Business logic and analytics views
│   ├── urls.py        # App URL configuration
│   └── templates/     # HTML templates
├── users/             # User management app
├── templates/         # Global templates
├── static/            # Static files (CSS, images)
├── docker-compose.yml # Docker configuration
├── Dockerfile         # Docker container definition
└── requirements.txt   # Python dependencies
```

## 🛠️ Tech Stack

- **Backend:** Django 4.2, Django REST Framework
- **Database:** PostgreSQL (production), SQLite (development)
- **Authentication:** Django Allauth
- **Frontend:** Django Templates, Bootstrap 5
- **Charts:** Chart.js for interactive visualizations
- **Deployment:** Docker, Docker Compose, Nginx
- **Caching:** Redis
- **File Processing:** OpenPyXL, ReportLab

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ericyng/networthtracker.git
   cd networthtracker
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Web app: http://localhost:8000
   - Analytics: http://localhost:8000/dashboard/analytics/
   - Admin panel: http://localhost:8000/admin

### Docker Deployment

1. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Access the application**
   - Web app: http://localhost:8080
   - Analytics: http://localhost:8080/dashboard/analytics/

## 📊 Analytics Dashboard

The analytics page provides comprehensive financial insights:

### Key Metrics
- **Net Worth:** Current total net worth
- **Savings Rate:** Percentage of income saved
- **Emergency Fund:** Months of expenses covered
- **Asset Diversity:** Number of different asset types

### Charts and Visualizations
- **Net Worth Trends:** Line chart showing net worth over time
- **Asset Allocation:** Doughnut chart of asset distribution
- **Income vs Expenses:** Bar chart comparing monthly income and expenses
- **Spending by Category:** Pie chart of expense categories
- **Account Performance:** Line chart tracking individual account growth

### Financial Ratios
- **Debt-to-Income Ratio:** Total debt as percentage of assets
- **Emergency Fund Ratio:** Liquid assets vs monthly expenses
- **Asset Diversity Score:** Number of different asset types
- **Savings Rate:** Net savings as percentage of income

## 📈 Data Models

### Account
- User ownership and account details
- Account types: checking, savings, investment, loan, credit, other
- Classifications: pre-tax, post-tax, Roth, traditional, 401k, 529, HSA, FSA, taxable, debts
- Asset types: cash, crypto, property, vehicles, jewelry, art, electronics, furniture, clothing, books, sports, tools

### Transaction
- Income, expense, and transfer tracking
- Categories: salary, freelance, investment, food, transportation, housing, utilities, entertainment, shopping, healthcare, education, travel, other
- Account linking and date tracking

### AccountEntry
- Monthly balance snapshots
- Historical balance tracking
- Notes and metadata

## 🔗 URL Endpoints

- `/` - Redirects to dashboard
- `/dashboard/` - Main dashboard
- `/dashboard/analytics/` - **Analytics page with charts**
- `/dashboard/accounts/` - Account management
- `/dashboard/transactions/` - Transaction management
- `/dashboard/settings/` - User settings
- `/admin/` - Django admin interface

## 🔒 Security

- User authentication with Django Allauth
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password handling
- User-specific data isolation

## 📱 Features in Detail

### Analytics Calculations
- **Net Worth Trends:** Monthly calculation of total assets minus liabilities
- **Asset Allocation:** Percentage breakdown by asset type
- **Income vs Expenses:** Monthly aggregation and comparison
- **Spending Analysis:** Category-based expense analysis
- **Financial Ratios:** Automated calculation of key metrics
- **Growth Tracking:** Account performance over time

### Data Export
- **CSV Export:** Raw data export
- **Excel Export:** Formatted reports with charts
- **PDF Export:** Professional reports
- **Analytics Export:** JSON export of chart data

### User Experience
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Interactive Charts:** Hover effects and tooltips
- **Real-time Updates:** Live data calculations
- **Export Functionality:** Download analytics data
- **Navigation:** Easy access to all features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation
- Review the analytics calculations

## 🔄 Future Enhancements

- **Mobile Application:** React Native mobile app
- **API Endpoints:** RESTful API for external integrations
- **Real-time Updates:** WebSocket-based real-time data
- **Advanced Analytics:** Machine learning insights
- **Multi-user Support:** Family/shared account management
- **Investment Tracking:** Real-time investment data integration
- **Budget Planning:** Budget creation and tracking
- **Goal Setting:** Financial goal management

---

**Net Worth Tracker** - Take control of your financial future with comprehensive tracking and analytics.
