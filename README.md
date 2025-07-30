# 💰 NetWorth Tracker

A comprehensive personal finance tracking application built with Django that helps you monitor your net worth, track account balances, and manage your financial portfolio.

## 🚀 Features

### 📊 **Dashboard & Analytics**
- **Dual Chart Dashboard**: Time series bar chart for net worth trends + pie chart for account distribution
- **Real-time Net Worth Tracking**: Monitor your total financial position over time
- **Account Classification**: Organize accounts by type, tax classification, and asset category
- **Historical Balance Tracking**: Monthly balance snapshots for trend analysis

### 🏦 **Account Management**
- **Multiple Account Types**: Checking, savings, credit cards, investments, loans, and more
- **Tax Classification**: Pre-tax, post-tax, Roth, Traditional IRA, 401(k), HSA, FSA, and taxable accounts
- **Asset Categories**: Cash, real estate, vehicles, jewelry, art, electronics, and more
- **Institution Tracking**: Link accounts to financial institutions

### 📈 **Financial Tracking**
- **Monthly Balance Entries**: Track account balances month by month
- **Transaction Management**: Record income, expenses, and transfers
- **Category-based Transactions**: Detailed categorization for spending analysis
- **Historical Data**: Complete financial history and trend analysis

### 🔐 **Authentication & Security**
- **Traditional Login**: Username/email and password authentication
- **Social Authentication**: Google and Facebook sign-in options
- **User Profiles**: Manage personal information and account settings
- **Data Privacy**: Secure user data with proper authentication

### ⚙️ **User Management**
- **Account Settings**: Update profile information and preferences
- **Data Management**: Bulk operations for accounts, transactions, and entries
- **Statistics Dashboard**: View account counts, transaction history, and usage metrics

## 🛠️ Technology Stack

- **Backend**: Django 4.2.23
- **Database**: SQLite (development), supports PostgreSQL/MySQL (production)
- **Authentication**: Django Allauth with social authentication
- **Frontend**: Bootstrap 5, Chart.js for data visualization
- **Icons**: Bootstrap Icons
- **Template Engine**: Django Template Language (DTL)

## 📋 Prerequisites

- Python 3.9+
- pip (Python package installer)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/networth-tracker.git
cd networth-tracker
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

### 4. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login Page**: http://127.0.0.1:8000/accounts/login/

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Social Authentication Setup
For Google and Facebook login, follow the setup guide in `SOCIAL_AUTH_SETUP.md`.

## 📊 Data Models

### Core Models
- **User**: Django's built-in user model
- **Account**: Financial accounts with classification and asset types
- **AccountEntry**: Monthly balance snapshots for net worth tracking
- **Transaction**: Individual financial transactions with categorization

### Account Classifications
- **Tax-Advantaged**: Pre-tax, Roth, Traditional IRA, 401(k), HSA, FSA
- **Standard**: Post-tax, taxable accounts
- **Asset Types**: Cash, property, vehicles, jewelry, art, electronics, etc.

## 🎯 Usage Guide

### Getting Started
1. **Register/Login**: Create an account or sign in
2. **Add Accounts**: Create your first financial account
3. **Set Balances**: Add monthly balance entries for each account
4. **Track Transactions**: Record income and expenses
5. **Monitor Dashboard**: View your net worth trends and account distribution

### Account Management
- **Create Accounts**: Add checking, savings, investment, and other accounts
- **Classify Accounts**: Use appropriate tax classifications and asset types
- **Update Balances**: Add monthly balance entries for accurate tracking
- **Link Institutions**: Associate accounts with financial institutions

### Data Analysis
- **Net Worth Trends**: View your financial growth over time
- **Account Distribution**: See how your assets are allocated
- **Transaction History**: Track spending patterns and income sources
- **Category Analysis**: Analyze spending by category

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **Secure Authentication**: Django Allauth security features
- **Password Validation**: Strong password requirements

## 🚀 Deployment

### Production Setup
1. **Database**: Configure PostgreSQL or MySQL
2. **Static Files**: Collect and serve static files
3. **Environment**: Set production environment variables
4. **HTTPS**: Configure SSL certificates
5. **Web Server**: Set up Nginx/Apache with Gunicorn

### Environment Variables (Production)
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the inline code comments and docstrings
- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Use GitHub Discussions for questions and ideas

## 🎉 Acknowledgments

- **Django**: The web framework for perfectionists with deadlines
- **Bootstrap**: The most popular CSS framework for responsive web design
- **Chart.js**: Simple yet flexible JavaScript charting library
- **Django Allauth**: Integrated set of Django applications addressing authentication

---

**Built with ❤️ for personal finance management**
