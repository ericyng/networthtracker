# Net Worth Tracker

A comprehensive personal finance management application that helps you track your net worth, manage accounts, and monitor your financial progress over time.

## 🚀 Features

### Core Functionality
- **Net Worth Tracking:** Monitor your total net worth with monthly snapshots
- **Account Management:** Track multiple account types (checking, savings, investments, loans, etc.)
- **Transaction Tracking:** Record income, expenses, and transfers
- **Financial Analytics:** Visualize your financial progress with charts and reports
- **Data Export:** Export your data in CSV, Excel, and PDF formats
- **Multi-Currency Support:** Track accounts in different currencies
- **Asset Classification:** Categorize assets by type (cash, crypto, property, etc.)

### Account Types Supported
- **Banking:** Checking, Savings, Credit Cards
- **Investments:** 401(k), IRA, Roth IRA, 529 Plans, HSA, FSA
- **Assets:** Real Estate, Vehicles, Jewelry, Art, Electronics
- **Liabilities:** Loans, Credit Cards, Mortgages

## 🏗️ Project Structure

```
networthtracker/
├── backend/           # Django backend application
│   ├── settings.py    # Django settings
│   ├── urls.py        # Main URL configuration
│   └── wsgi.py        # WSGI configuration
├── dashboard/         # Main dashboard app
│   ├── models.py      # Data models (Account, Transaction, AccountEntry)
│   ├── views.py       # Business logic and views
│   ├── forms.py       # Form definitions
│   └── templates/     # HTML templates
├── users/             # User management app
├── static/            # Static files (CSS, images)
├── templates/         # Global templates
├── docker-compose.yml # Docker Compose configuration
├── Dockerfile         # Docker container definition
└── requirements.txt   # Python dependencies
```

## 🛠️ Tech Stack

- **Backend:** Django 4.2, Django REST Framework
- **Database:** PostgreSQL (production), SQLite (development)
- **Authentication:** Django Allauth
- **Frontend:** Django Templates, Bootstrap CSS
- **Charts:** Chart.js (via CDN)
- **Deployment:** Docker, Docker Compose, Nginx
- **Caching:** Redis
- **File Processing:** OpenPyXL, ReportLab

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd networthtracker
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Web app: http://localhost:8080
   - Admin panel: http://localhost:8080/admin

### Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

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

## 🔧 Configuration

### Environment Variables
- `DEBUG`: Django debug mode
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `REDIS_URL`: Redis connection string

### Docker Configuration
The application uses Docker Compose with the following services:
- **web:** Django application
- **db:** PostgreSQL database
- **nginx:** Reverse proxy
- **redis:** Caching and sessions

## 📈 Features in Detail

### Dashboard
- Net worth overview with charts
- Account balances summary
- Recent transactions
- Monthly progress tracking

### Account Management
- Create, edit, and delete accounts
- Track account balances over time
- Categorize accounts by type and classification
- Support for multiple currencies

### Transaction Tracking
- Record income, expenses, and transfers
- Categorize transactions
- Link transactions to specific accounts
- Transaction history and reporting

### Data Export
- **CSV Export:** Raw data export
- **Excel Export:** Formatted reports with charts
- **PDF Export:** Professional reports

### Data Management
- Bulk import from CSV/Excel files
- Data validation and error handling
- Duplicate detection and cleanup
- Data backup and restore

## 🔒 Security

- User authentication with Django Allauth
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password handling

## 🚀 Deployment

### Production Deployment
1. Set up a production server with Docker
2. Configure environment variables
3. Set up SSL certificates
4. Configure domain and DNS
5. Run `docker-compose -f docker-compose.prod.yml up -d`

### Environment-Specific Settings
- `development_settings.py`: Development configuration
- `docker_settings.py`: Docker environment configuration
- `production_settings.py`: Production configuration

## 📝 API Endpoints

The application provides web-based interface with the following main endpoints:

- `/dashboard/` - Main dashboard
- `/dashboard/accounts/` - Account management
- `/dashboard/transactions/` - Transaction management
- `/dashboard/entries/` - Account entries management
- `/dashboard/settings/` - User settings
- `/dashboard/data-management/` - Data import/export
- `/admin/` - Django admin interface

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
- Contact the development team
- Check the documentation in the `/docs/` directory

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Core net worth tracking functionality
- Account and transaction management
- Data export capabilities
- Docker deployment support
