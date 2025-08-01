# Net Worth Tracker - Application Design

## Overview

The Net Worth Tracker is a comprehensive personal finance management application built with Django that helps users track their net worth, manage accounts, and monitor financial progress over time.

## Application Architecture

### Technology Stack
- **Backend Framework:** Django 4.2
- **Database:** PostgreSQL (production), SQLite (development)
- **Authentication:** Django Allauth
- **Frontend:** Django Templates with Bootstrap
- **Charts:** Chart.js (CDN)
- **Deployment:** Docker, Docker Compose, Nginx
- **Caching:** Redis
- **File Processing:** OpenPyXL, ReportLab

### Core Components

#### 1. User Management (`users/`)
- Custom user model extensions
- Authentication views and forms
- Social authentication support (currently disabled)

#### 2. Dashboard Application (`dashboard/`)
- Main application logic
- Data models and business logic
- Views and templates
- Data import/export functionality

#### 3. Backend Configuration (`backend/`)
- Django project settings
- URL routing
- WSGI/ASGI configuration

## Data Models

### Account Model
```python
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_type = models.CharField(choices=ACCOUNT_TYPES)
    classification = models.CharField(choices=CLASSIFICATION_TYPES)
    asset_type = models.CharField(choices=ASSET_TYPES)
    currency = models.CharField(max_length=3, default='USD')
    institution = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
```

**Account Types:**
- checking, savings, credit, investment, loan, other

**Classifications:**
- pretax, posttax, roth, traditional, 401k, 529, hsa, fsa, taxable, debts, other

**Asset Types:**
- cash, crypto, property, vehicles, jewelry, art, electronics, furniture, clothing, books, sports, tools, other

### Transaction Model
```python
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES)
    category = models.CharField(choices=CATEGORIES)
    description = models.CharField(max_length=200)
    date = models.DateField()
```

**Transaction Types:**
- income, expense, transfer

**Categories:**
- salary, freelance, investment, food, transportation, housing, utilities, entertainment, shopping, healthcare, education, travel, other

### AccountEntry Model
```python
class AccountEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    month = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    year = models.IntegerField()
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    notes = models.TextField(blank=True)
```

## URL Structure

### Main Application URLs
```
/                           # Redirects to dashboard landing
/dashboard/                  # Main dashboard
/dashboard/accounts/         # Account management
/dashboard/transactions/     # Transaction management
/dashboard/entries/          # Account entries management
/dashboard/settings/         # User settings
/dashboard/data-management/  # Data import/export
/admin/                      # Django admin interface
```

### Authentication URLs (Django Allauth)
```
/accounts/login/             # User login
/accounts/logout/            # User logout
/accounts/signup/            # User registration
/accounts/password/reset/    # Password reset
```

## Core Features

### 1. Dashboard Overview
- **Net Worth Summary:** Total assets minus liabilities
- **Account Balances:** Current balances by account type
- **Monthly Progress:** Net worth changes over time
- **Recent Transactions:** Latest financial activity
- **Charts:** Visual representation of financial data

### 2. Account Management
- **Create/Edit Accounts:** Add new accounts or modify existing ones
- **Account Types:** Support for various financial account types
- **Balance Tracking:** Monthly balance snapshots
- **Account Classification:** Tax-advantaged account identification
- **Asset Categorization:** Detailed asset type classification

### 3. Transaction Tracking
- **Income/Expense Recording:** Track all financial transactions
- **Transaction Categories:** Organized spending and income tracking
- **Account Linking:** Associate transactions with specific accounts
- **Transaction History:** Complete financial activity log

### 4. Data Management
- **Bulk Import:** Import data from CSV/Excel files
- **Data Export:** Export in CSV, Excel, and PDF formats
- **Data Validation:** Error checking and duplicate detection
- **Data Cleanup:** Tools for maintaining data integrity

### 5. Financial Analytics
- **Net Worth Trends:** Track progress over time
- **Account Performance:** Individual account analysis
- **Spending Patterns:** Transaction category analysis
- **Asset Allocation:** Portfolio breakdown by asset type

## Business Logic

### Net Worth Calculation
```python
def calculate_net_worth(user, month=None, year=None):
    """
    Calculate total net worth for a user at a specific time period
    """
    accounts = Account.objects.filter(user=user, is_active=True)
    total_assets = 0
    total_liabilities = 0
    
    for account in accounts:
        balance = account.get_latest_balance(month, year)
        if account.account_type in ['loan', 'credit']:
            total_liabilities += abs(balance)
        else:
            total_assets += balance
    
    return total_assets - total_liabilities
```

### Data Import Processing
- **CSV/Excel Parsing:** Flexible file format support
- **Data Validation:** Check for required fields and data types
- **Duplicate Detection:** Identify and handle duplicate entries
- **Error Handling:** Graceful handling of import errors

### Export Functionality
- **CSV Export:** Raw data export for external analysis
- **Excel Export:** Formatted reports with charts and summaries
- **PDF Export:** Professional reports for sharing or printing

## Security Features

### Authentication & Authorization
- **User Authentication:** Secure login/logout system
- **Session Management:** Secure session handling
- **Permission System:** User-specific data access
- **CSRF Protection:** Cross-site request forgery prevention

### Data Security
- **Input Validation:** Sanitize all user inputs
- **SQL Injection Prevention:** Use Django ORM
- **XSS Protection:** Template auto-escaping
- **Secure Headers:** Security middleware configuration

## Deployment Architecture

### Docker Configuration
```yaml
services:
  web:          # Django application
  db:           # PostgreSQL database
  nginx:        # Reverse proxy
  redis:        # Caching and sessions
```

### Environment Configuration
- **Development:** Local development with SQLite
- **Docker:** Containerized deployment with PostgreSQL
- **Production:** Production-optimized settings

### Performance Optimization
- **Database Indexing:** Optimized queries
- **Caching:** Redis-based caching
- **Static Files:** CDN-ready static file serving
- **Database Connection Pooling:** Efficient database connections

## API Endpoints (Web Interface)

### Dashboard Views
- `GET /dashboard/` - Main dashboard with net worth overview
- `GET /dashboard/accounts/` - Account listing and management
- `GET /dashboard/transactions/` - Transaction listing and management
- `GET /dashboard/entries/` - Account entries management

### Data Management
- `GET /dashboard/data-management/` - Data import/export interface
- `POST /dashboard/data-management/` - File upload and processing
- `GET /dashboard/export/{format}/{data_type}/` - Data export endpoints

### User Management
- `GET /dashboard/settings/` - User settings and preferences
- `POST /dashboard/settings/` - Update user settings

## Error Handling

### Data Validation
- **Form Validation:** Django form validation
- **Model Validation:** Database constraint enforcement
- **Business Logic Validation:** Custom validation rules
- **User Feedback:** Clear error messages and guidance

### Exception Handling
- **Database Errors:** Graceful database error handling
- **File Processing Errors:** Import/export error management
- **Authentication Errors:** Secure authentication failure handling
- **Permission Errors:** Access control enforcement

## Monitoring and Logging

### Application Logging
- **Request Logging:** Track user activity
- **Error Logging:** Capture and log errors
- **Performance Monitoring:** Track application performance
- **Security Logging:** Monitor security events

### Health Checks
- **Database Connectivity:** Database health monitoring
- **Redis Connectivity:** Cache service monitoring
- **Application Status:** Overall application health
- **Docker Health Checks:** Container health monitoring

## Future Enhancements

### Planned Features
- **Mobile Application:** React Native mobile app
- **API Endpoints:** RESTful API for external integrations
- **Real-time Updates:** WebSocket-based real-time data
- **Advanced Analytics:** Machine learning insights
- **Multi-user Support:** Family/shared account management
- **Investment Tracking:** Real-time investment data integration
- **Budget Planning:** Budget creation and tracking
- **Goal Setting:** Financial goal management

### Technical Improvements
- **Microservices Architecture:** Service decomposition
- **Event-driven Architecture:** Asynchronous processing
- **Advanced Caching:** Multi-level caching strategy
- **Performance Optimization:** Query optimization and indexing
- **Security Enhancements:** Advanced security features 