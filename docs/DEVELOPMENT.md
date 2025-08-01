# Net Worth Tracker - Development Guide

## Overview

This guide covers setting up and developing the Net Worth Tracker application locally. The application is built with Django and uses PostgreSQL for the database.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)
- Git
- Virtual environment tool (venv, conda, etc.)

## Local Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd networthtracker
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### PostgreSQL Setup
```bash
# Create database
createdb networthtracker_dev

# Or using psql
psql -U postgres
CREATE DATABASE networthtracker_dev;
CREATE USER networthtracker_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE networthtracker_dev TO networthtracker_user;
\q
```

#### Environment Configuration
Create a `.env` file in the project root:
```bash
DEBUG=True
SECRET_KEY=your-development-secret-key
DATABASE_URL=postgresql://networthtracker_user:your_password@localhost:5432/networthtracker_dev
REDIS_URL=redis://localhost:6379/1
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Django Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start development server
python manage.py runserver
```

### 6. Access the Application
- Web application: http://localhost:8000
- Admin panel: http://localhost:8000/admin

## Project Structure

```
networthtracker/
├── backend/                 # Django project configuration
│   ├── settings.py         # Main settings file
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── dashboard/              # Main application
│   ├── models.py           # Data models
│   ├── views.py            # View functions
│   ├── forms.py            # Form definitions
│   ├── urls.py             # App URL configuration
│   ├── admin.py            # Admin interface
│   ├── tests.py            # Test cases
│   └── templates/          # HTML templates
├── users/                  # User management app
│   ├── models.py           # User model extensions
│   ├── views.py            # User views
│   └── adapters.py         # Allauth adapters
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   └── images/            # Images
├── templates/              # Global templates
├── docs/                   # Documentation
├── logs/                   # Application logs
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── docker-compose.yml     # Docker configuration
```

## Development Workflow

### 1. Code Style and Standards

#### Python Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Use flake8 for linting
- Maximum line length: 88 characters

#### Django Best Practices
- Use Django's built-in features
- Follow Django naming conventions
- Use Django forms for data validation
- Implement proper model relationships

### 2. Database Management

#### Creating Migrations
```bash
# Create migration for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

#### Database Seeding
```bash
# Create sample data
python manage.py shell
```

Example seeding script:
```python
from django.contrib.auth.models import User
from dashboard.models import Account, Transaction, AccountEntry
from decimal import Decimal

# Create test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Create sample accounts
checking = Account.objects.create(
    user=user,
    name='Main Checking',
    account_type='checking',
    classification='posttax',
    asset_type='cash',
    institution='Bank of America'
)

savings = Account.objects.create(
    user=user,
    name='Emergency Fund',
    account_type='savings',
    classification='posttax',
    asset_type='cash',
    institution='Bank of America'
)

# Create sample transactions
Transaction.objects.create(
    user=user,
    account=checking,
    amount=Decimal('5000.00'),
    transaction_type='income',
    category='salary',
    description='Monthly salary',
    date='2024-01-15'
)

# Create sample account entries
AccountEntry.objects.create(
    account=checking,
    month=1,
    year=2024,
    balance=Decimal('5000.00'),
    notes='January balance'
)
```

### 3. Testing

#### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test dashboard

# Run specific test file
python manage.py test dashboard.tests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

#### Writing Tests
```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from dashboard.models import Account, Transaction
from decimal import Decimal

class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_account_creation(self):
        account = Account.objects.create(
            user=self.user,
            name='Test Account',
            account_type='checking',
            classification='posttax',
            asset_type='cash'
        )
        self.assertEqual(account.name, 'Test Account')
        self.assertEqual(account.account_type, 'checking')

class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_dashboard_requires_login(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        
    def test_dashboard_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
```

### 4. Debugging

#### Django Debug Toolbar
Add to `INSTALLED_APPS` in development settings:
```python
INSTALLED_APPS = [
    # ... existing apps
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... existing middleware
]

INTERNAL_IPS = [
    '127.0.0.1',
]
```

#### Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'dashboard': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### 5. Performance Optimization

#### Database Optimization
```python
# Use select_related for foreign keys
accounts = Account.objects.select_related('user').all()

# Use prefetch_related for many-to-many
transactions = Transaction.objects.prefetch_related('account').all()

# Use only() to limit fields
accounts = Account.objects.only('name', 'account_type').all()

# Use defer() to exclude fields
accounts = Account.objects.defer('notes').all()
```

#### Caching
```python
from django.core.cache import cache
from django.views.decorators.cache import cache_page

# View-level caching
@cache_page(60 * 15)  # Cache for 15 minutes
def dashboard(request):
    # View logic here
    pass

# Function-level caching
def get_net_worth(user_id):
    cache_key = f"net_worth_{user_id}"
    net_worth = cache.get(cache_key)
    
    if net_worth is None:
        # Calculate net worth
        net_worth = calculate_net_worth(user_id)
        cache.set(cache_key, net_worth, 300)  # Cache for 5 minutes
    
    return net_worth
```

## Code Organization

### Models
- Keep models focused and single-purpose
- Use proper field types and constraints
- Implement model methods for business logic
- Use Meta classes for ordering and constraints

### Views
- Use function-based views for simple operations
- Use class-based views for complex operations
- Implement proper error handling
- Use Django messages for user feedback

### Forms
- Create forms for data validation
- Use ModelForms when possible
- Implement custom validation methods
- Handle form errors gracefully

### Templates
- Use template inheritance
- Keep templates simple and focused
- Use template tags for complex logic
- Implement proper escaping

## Git Workflow

### Branch Strategy
```bash
# Create feature branch
git checkout -b feature/account-management

# Make changes and commit
git add .
git commit -m "Add account management functionality"

# Push to remote
git push origin feature/account-management

# Create pull request
# Merge after review
```

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 50 characters
- Use body to explain what and why, not how

### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No security vulnerabilities
- [ ] Performance considerations addressed
- [ ] Error handling is implemented
- [ ] User experience is considered

## Common Development Tasks

### Adding New Models
1. Define model in `models.py`
2. Create and run migrations
3. Register in admin interface
4. Create forms if needed
5. Add views and templates
6. Update URL configuration
7. Write tests

### Adding New Views
1. Create view function/class
2. Add URL pattern
3. Create template
4. Add tests
5. Update documentation

### Data Import/Export
1. Create management commands
2. Implement file processing
3. Add validation
4. Handle errors gracefully
5. Provide user feedback

## Troubleshooting

### Common Issues

#### Database Connection
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U networthtracker_user -d networthtracker_dev -h localhost
```

#### Migration Issues
```bash
# Reset migrations (development only)
python manage.py migrate dashboard zero
rm dashboard/migrations/0*.py
python manage.py makemigrations dashboard
python manage.py migrate
```

#### Static Files
```bash
# Collect static files
python manage.py collectstatic --clear

# Check static file settings
python manage.py findstatic css/master.css
```

#### Environment Variables
```bash
# Check environment variables
python manage.py shell
import os
print(os.environ.get('DEBUG'))
```

## Development Tools

### Recommended Extensions (VS Code)
- Python
- Django
- GitLens
- Python Docstring Generator
- Python Test Explorer

### Useful Commands
```bash
# Django shell
python manage.py shell

# Django shell with IPython
python manage.py shell_plus

# Check for problems
python manage.py check

# Validate models
python manage.py validate

# Show SQL for query
python manage.py shell
from django.db import connection
# Run your query
print(connection.queries)
```

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/) 