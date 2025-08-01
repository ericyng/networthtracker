#!/bin/bash

# Setup script for NetWorth Tracker development aliases
# This script adds convenient aliases to your shell configuration

echo "🔧 Setting up NetWorth Tracker development aliases..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[SETUP]${NC} $1"
}

# Get the current shell
CURRENT_SHELL=$(basename "$SHELL")

# Determine which config file to use
if [ "$CURRENT_SHELL" = "zsh" ]; then
    CONFIG_FILE="$HOME/.zshrc"
    print_info "Detected zsh shell, using ~/.zshrc"
elif [ "$CURRENT_SHELL" = "bash" ]; then
    CONFIG_FILE="$HOME/.bashrc"
    print_info "Detected bash shell, using ~/.bashrc"
else
    CONFIG_FILE="$HOME/.bashrc"
    print_warning "Unknown shell, defaulting to ~/.bashrc"
fi

# Get the absolute path to the project directory
PROJECT_DIR=$(pwd)
print_info "Project directory: $PROJECT_DIR"

# Create the aliases
ALIASES=(
    "# NetWorth Tracker Development Aliases"
    "alias nwt-dev='cd $PROJECT_DIR && ./dev.sh'"
    "alias nwt-run='cd $PROJECT_DIR && python manage.py runserver --settings=backend.development_settings'"
    "alias nwt-migrate='cd $PROJECT_DIR && python manage.py migrate --settings=backend.development_settings'"
    "alias nwt-shell='cd $PROJECT_DIR && python manage.py shell --settings=backend.development_settings'"
    "alias nwt-collect='cd $PROJECT_DIR && python manage.py collectstatic --noinput --settings=backend.development_settings'"
    "alias nwt-admin='cd $PROJECT_DIR && python manage.py createsuperuser --settings=backend.development_settings'"
    ""
)

# Check if aliases already exist
if grep -q "nwt-dev" "$CONFIG_FILE" 2>/dev/null; then
    print_warning "Aliases already exist in $CONFIG_FILE"
    print_info "Skipping alias creation"
else
    # Add aliases to the config file
    print_info "Adding aliases to $CONFIG_FILE..."
    echo "" >> "$CONFIG_FILE"
    for alias in "${ALIASES[@]}"; do
        echo "$alias" >> "$CONFIG_FILE"
    done
    print_status "Aliases added successfully!"
fi

# Create a quick reference file
print_info "Creating quick reference..."
cat > DEV_QUICK_REFERENCE.md << 'EOF'
# NetWorth Tracker Development Quick Reference

## Available Aliases

After running `./setup_aliases.sh`, you can use these convenient aliases:

- `nwt-dev` - Start the development server (recommended)
- `nwt-run` - Quick start development server
- `nwt-migrate` - Run database migrations
- `nwt-shell` - Open Django shell
- `nwt-collect` - Collect static files
- `nwt-admin` - Create superuser

## Manual Commands

If you prefer manual commands:

```bash
# Start development server
python manage.py runserver --settings=backend.development_settings

# Run migrations
python manage.py migrate --settings=backend.development_settings

# Create superuser
python manage.py createsuperuser --settings=backend.development_settings
```

## URLs

- **Main site**: http://127.0.0.1:8000
- **Landing page**: http://127.0.0.1:8000/dashboard/landing/
- **Login page**: http://127.0.0.1:8000/accounts/login/
- **Signup disabled**: http://127.0.0.1:8000/dashboard/signup-disabled/

## Notes

- Development settings disable HTTPS redirects
- All security settings are relaxed for local development
- Virtual environment is automatically activated
- Static files are automatically collected
EOF

print_status "Setup complete! 🎉"
echo ""
print_info "To use the new aliases, either:"
print_info "1. Restart your terminal, or"
print_info "2. Run: source $CONFIG_FILE"
echo ""
print_info "Then you can use: nwt-dev"
echo ""
print_info "Quick reference saved to: DEV_QUICK_REFERENCE.md" 