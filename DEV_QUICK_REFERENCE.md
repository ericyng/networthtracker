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
