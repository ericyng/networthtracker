# Net Worth Tracker Backend API

Django REST Framework API for the Net Worth Tracker personal finance management application.

## 🚀 Features

### Core API Endpoints
- **Authentication:** User registration and login
- **Accounts:** Manage financial accounts (checking, savings, investments, loans)
- **Transactions:** Track income, expenses, and transfers
- **Account Entries:** Monthly balance snapshots for net worth tracking
- **Data Export:** Export financial data in various formats
- **Analytics:** Financial progress tracking and reporting

### Data Models
- **User:** User accounts and authentication
- **Account:** Financial accounts with types and classifications
- **Transaction:** Income, expense, and transfer records
- **AccountEntry:** Monthly balance snapshots for tracking net worth over time

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- PostgreSQL (production) or SQLite (development)
- Redis (optional, for caching)

### Installation

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

## 📚 API Documentation

### Authentication
- **POST** `/accounts/login/` - User login
- **POST** `/accounts/signup/` - User registration
- **POST** `/accounts/logout/` - User logout

### Dashboard
- **GET** `/dashboard/` - Main dashboard view
- **GET** `/dashboard/accounts/` - List user accounts
- **GET** `/dashboard/transactions/` - List transactions
- **GET** `/dashboard/entries/` - List account entries

### Accounts
- **GET** `/dashboard/accounts/` - List user accounts
- **POST** `/dashboard/accounts/create/` - Create new account
- **GET** `/dashboard/accounts/{id}/` - Get account details
- **POST** `/dashboard/accounts/{id}/edit/` - Update account
- **POST** `/dashboard/accounts/{id}/delete/` - Delete account

### Transactions
- **GET** `/dashboard/transactions/` - List transactions
- **POST** `/dashboard/transactions/create/` - Create new transaction
- **GET** `/dashboard/transactions/{id}/` - Get transaction details
- **POST** `/dashboard/transactions/{id}/edit/` - Update transaction
- **POST** `/dashboard/transactions/{id}/delete/` - Delete transaction

### Account Entries
- **GET** `/dashboard/entries/` - List account entries
- **POST** `/dashboard/entries/create/` - Create new entry
- **GET** `/dashboard/entries/{id}/` - Get entry details
- **POST** `/dashboard/entries/{id}/edit/` - Update entry
- **POST** `/dashboard/entries/{id}/delete/` - Delete entry

### Data Management
- **GET** `/dashboard/data-management/` - Data management interface
- **POST** `/dashboard/data-management/export/` - Export data
- **POST** `/dashboard/data-management/import/` - Import data

## 🔧 Configuration

### Environment Variables
```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost/networthtracker

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test dashboard.tests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False`
2. Configure production database
3. Set up static file serving
4. Configure web server (Nginx + Gunicorn)
5. Set up SSL certificates

### Docker Deployment
```bash
docker-compose up -d
```

## 📝 Development

### Code Style
- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting

### Pre-commit Hooks
```bash
pre-commit install
```

## 🔒 Security

- Django Allauth authentication
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password handling

## 📊 Data Models

### Account
- **User:** Owner of the account
- **Name:** Account name
- **Type:** Checking, Savings, Investment, Loan, etc.
- **Classification:** Pre-tax, Post-tax, Roth, Traditional IRA, etc.
- **Asset Type:** Cash, Crypto, Property, Vehicles, etc.
- **Currency:** USD, EUR, etc.
- **Institution:** Bank or financial institution name
- **Account Number:** Account identifier (optional)

### Transaction
- **User:** Owner of the transaction
- **Account:** Associated account
- **Amount:** Transaction amount
- **Type:** Income, Expense, Transfer
- **Category:** Salary, Food, Transportation, etc.
- **Description:** Transaction description
- **Date:** Transaction date

### AccountEntry
- **Account:** Associated account
- **Month/Year:** Monthly snapshot period
- **Balance:** Account balance for the period
- **Notes:** Additional notes 