# Net Worth Tracker - Quick Reference

## 🚀 Quick Start Commands

### Docker Deployment
```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker-compose logs -f web

# Access container
docker-compose exec web bash
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver

# Collect static files
python manage.py collectstatic
```

## 📊 Data Models

### Account Types
- `checking` - Checking accounts
- `savings` - Savings accounts
- `credit` - Credit cards
- `investment` - Investment accounts
- `loan` - Loans and mortgages
- `other` - Other accounts

### Account Classifications
- `pretax` - Pre-tax accounts
- `posttax` - Post-tax accounts
- `roth` - Roth IRA
- `traditional` - Traditional IRA
- `401k` - 401(k) accounts
- `529` - 529 education plans
- `hsa` - Health Savings Accounts
- `fsa` - Flexible Spending Accounts
- `taxable` - Taxable investment accounts
- `debts` - Debt accounts
- `other` - Other classifications

### Asset Types
- `cash` - Cash and cash equivalents
- `crypto` - Cryptocurrency
- `property` - Real estate
- `vehicles` - Cars, boats, etc.
- `jewelry` - Jewelry and watches
- `art` - Art and collectibles
- `electronics` - Electronics
- `furniture` - Furniture and appliances
- `clothing` - Clothing and accessories
- `books` - Books and media
- `sports` - Sports equipment
- `tools` - Tools and equipment
- `other` - Other assets

### Transaction Types
- `income` - Income transactions
- `expense` - Expense transactions
- `transfer` - Transfer transactions

### Transaction Categories
- `salary` - Salary income
- `freelance` - Freelance income
- `investment` - Investment income
- `food` - Food and dining
- `transportation` - Transportation
- `housing` - Housing expenses
- `utilities` - Utilities
- `entertainment` - Entertainment
- `shopping` - Shopping
- `healthcare` - Healthcare
- `education` - Education
- `travel` - Travel
- `other` - Other categories

## 🔗 URL Endpoints

### Main Application
- `/` - Redirects to dashboard
- `/dashboard/` - Main dashboard
- `/dashboard/accounts/` - Account management
- `/dashboard/transactions/` - Transaction management
- `/dashboard/entries/` - Account entries
- `/dashboard/settings/` - User settings
- `/dashboard/data-management/` - Data import/export
- `/admin/` - Django admin

### Authentication
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/accounts/signup/` - User registration
- `/accounts/password/reset/` - Password reset

### Export Endpoints
- `/dashboard/export/csv/accounts/` - Export accounts to CSV
- `/dashboard/export/csv/transactions/` - Export transactions to CSV
- `/dashboard/export/csv/entries/` - Export entries to CSV
- `/dashboard/export/excel/accounts/` - Export accounts to Excel
- `/dashboard/export/excel/transactions/` - Export transactions to Excel
- `/dashboard/export/excel/entries/` - Export entries to Excel
- `/dashboard/export/pdf/accounts/` - Export accounts to PDF
- `/dashboard/export/pdf/transactions/` - Export transactions to PDF
- `/dashboard/export/pdf/entries/` - Export entries to PDF

## 🛠️ Management Commands

### Available Commands
```bash
# Check for duplicate accounts
python manage.py check_duplicate_accounts

# Check for May entries
python manage.py check_may_entries

# Clean up duplicate accounts
python manage.py cleanup_duplicate_accounts

# Fix duplicate entries
python manage.py fix_duplicate_entries

# Test all charts
python manage.py test_all_charts

# Test combination chart
python manage.py test_combination_chart

# Test crypto categorization
python manage.py test_crypto_categorization
```

## 📁 File Structure

### Key Files
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Docker configuration
- `Dockerfile` - Docker container definition
- `nginx.conf` - Nginx configuration
- `.env` - Environment variables (create from env.example)

### Important Directories
- `backend/` - Django project configuration
- `dashboard/` - Main application
- `users/` - User management
- `static/` - Static files (CSS, images)
- `templates/` - HTML templates
- `docs/` - Documentation
- `logs/` - Application logs

## 🔧 Configuration

### Environment Variables
```bash
DEBUG=True/False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://host:port/db
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

### Settings Files
- `backend/settings.py` - Main settings
- `backend/development_settings.py` - Development settings
- `backend/docker_settings.py` - Docker settings
- `backend/production_settings.py` - Production settings

## 🗄️ Database

### Tables
- `auth_user` - User accounts
- `dashboard_account` - Financial accounts
- `dashboard_transaction` - Financial transactions
- `dashboard_accountentry` - Monthly account balances

### Key Relationships
- User → Accounts (one-to-many)
- Account → Transactions (one-to-many)
- Account → AccountEntries (one-to-many)

## 📈 Business Logic

### Net Worth Calculation
```python
def calculate_net_worth(user, month=None, year=None):
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

### Account Balance Retrieval
```python
def get_latest_balance(self, month=None, year=None):
    if month is None or year is None:
        latest_entry = self.entries.order_by('-year', '-month').first()
    else:
        latest_entry = self.entries.filter(month=month, year=year).first()
    
    return latest_entry.balance if latest_entry else 0.00
```

## 🔒 Security

### Authentication
- Django Allauth for user authentication
- Session-based authentication
- CSRF protection enabled
- Secure password handling

### Data Protection
- User-specific data isolation
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## 📊 Data Import/Export

### Supported Formats
- CSV (Comma-separated values)
- Excel (XLSX format)
- PDF (Portable Document Format)

### Import Features
- Bulk data import
- Data validation
- Error handling
- Duplicate detection

### Export Features
- Formatted reports
- Charts and graphs
- Professional styling
- Multiple data types

## 🐳 Docker Services

### Service Names
- `web` - Django application
- `db` - PostgreSQL database
- `nginx` - Reverse proxy
- `redis` - Caching and sessions

### Ports
- `8080` - Web application (HTTP)
- `8443` - Web application (HTTPS)
- `5432` - PostgreSQL (internal)
- `6379` - Redis (internal)

### Volumes
- `postgres_data` - Database persistence
- `static_files` - Static assets
- `media_files` - User uploads
- `logs` - Application logs

## 🔍 Troubleshooting

### Common Issues
1. **Database connection errors** - Check PostgreSQL service
2. **Static files not loading** - Run collectstatic
3. **Migration errors** - Check migration status
4. **Permission errors** - Check file permissions

### Debug Commands
```bash
# Check Django status
python manage.py check

# Show migrations
python manage.py showmigrations

# Check static files
python manage.py findstatic css/master.css

# Django shell
python manage.py shell
```

### Log Locations
- Application logs: `logs/`
- Docker logs: `docker-compose logs`
- Nginx logs: Container logs
- Database logs: PostgreSQL logs

## 📞 Support

### Documentation
- Main README: `README.md`
- API Design: `docs/API_DESIGN.md`
- Deployment: `docs/DEPLOYMENT.md`
- Development: `docs/DEVELOPMENT.md`

### Resources
- Django Documentation: https://docs.djangoproject.com/
- Docker Documentation: https://docs.docker.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/

### Contact
- Create issues in GitHub repository
- Check documentation in `/docs/` directory
- Review troubleshooting section above 