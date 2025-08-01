#!/bin/bash

# GEN3RIC LABS Deployment Script
# This script deploys the latest changes from git to the server

set -e  # Exit on any error

echo "🚀 Starting deployment for GEN3RIC LABS..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're on the server (adjust path as needed)
if [ -d "/var/www/gen3ric-labs.com" ]; then
    print_status "Detected server environment"
    PROJECT_DIR="/var/www/gen3ric-labs.com"
else
    print_warning "Not on server - this script should be run on the server"
    print_status "For local testing, you can modify PROJECT_DIR variable"
    PROJECT_DIR="/var/www/gen3ric-labs.com"
fi

# Navigate to project directory
print_status "Navigating to project directory: $PROJECT_DIR"
cd "$PROJECT_DIR" || {
    print_error "Failed to navigate to project directory"
    exit 1
}

# Check if git repository exists
if [ ! -d ".git" ]; then
    print_error "Git repository not found in $PROJECT_DIR"
    exit 1
fi

# Backup current state (optional)
print_status "Creating backup of current state..."
cp -r . ../gen3ric-labs-backup-$(date +%Y%m%d-%H%M%S) 2>/dev/null || print_warning "Could not create backup"

# Pull latest changes from git
print_status "Pulling latest changes from git..."
git fetch origin
git reset --hard origin/main

# Check if pull was successful
if [ $? -eq 0 ]; then
    print_status "Successfully pulled latest changes"
else
    print_error "Failed to pull latest changes"
    exit 1
fi

# Set proper permissions (if on server)
if [ -d "/var/www" ]; then
    print_status "Setting proper permissions..."
    chown -R www-data:www-data "$PROJECT_DIR" 2>/dev/null || print_warning "Could not set ownership"
    chmod -R 755 "$PROJECT_DIR" 2>/dev/null || print_warning "Could not set permissions"
fi

# Restart web server if needed (uncomment if using systemd)
# print_status "Restarting web server..."
# systemctl reload nginx 2>/dev/null || print_warning "Could not reload nginx"

print_status "Deployment completed successfully! 🎉"
print_status "Your changes are now live at https://gen3ric-labs.com"

# Optional: Check if site is responding
print_status "Checking if site is responding..."
if curl -s -o /dev/null -w "%{http_code}" https://gen3ric-labs.com | grep -q "200\|301\|302"; then
    print_status "Site is responding correctly"
else
    print_warning "Site might not be responding correctly - check manually"
fi

echo ""
print_status "Deployment completed at $(date)" 