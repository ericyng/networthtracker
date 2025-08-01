#!/bin/bash

# NetWorth Tracker Development Server Script
# This script starts the Django development server with development settings

set -e

echo "🚀 Starting NetWorth Tracker Development Server..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[DEV]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    print_warning "manage.py not found in current directory"
    print_info "Make sure you're in the project root directory (pf/)"
    exit 1
fi

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    print_warning "Virtual environment not detected"
    print_info "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if development settings file exists
if [ ! -f "backend/development_settings.py" ]; then
    print_warning "Development settings file not found"
    print_info "Creating development settings..."
    cat > backend/development_settings.py << 'EOF'
"""
Development settings for backend project.
This file overrides production settings for local development.
"""

from .settings import *

# Override production settings for development
DEBUG = True

# Disable HTTPS redirects for development
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'

# Disable secure cookies for development
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Allow all hosts for development
ALLOWED_HOSTS = ['*']

print("🔧 Using development settings - HTTPS redirects disabled")
EOF
    print_status "Development settings created"
fi

# Run database migrations if needed
print_info "Checking database migrations..."
python manage.py migrate --settings=backend.development_settings

# Collect static files if needed
print_info "Collecting static files..."
python manage.py collectstatic --noinput --settings=backend.development_settings

print_status "Starting development server..."
print_info "Server will be available at: http://127.0.0.1:8000"
print_info "Landing page: http://127.0.0.1:8000/dashboard/landing/"
print_info "Login page: http://127.0.0.1:8000/accounts/login/"
print_info "Press Ctrl+C to stop the server"
echo ""

# Start the development server
python manage.py runserver --settings=backend.development_settings 