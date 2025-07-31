# NetWorth Tracker Deployment Guide

## Current Issues Fixed

### 1. HTTPS Security (Not Secure Icon)
- ✅ Added SSL/HTTPS configuration in Django settings
- ✅ Created production settings with security headers
- ✅ Added nginx configuration for SSL termination

### 2. Broken GEN3RIC Labs Logo
- ✅ Fixed logo references to use absolute HTTPS URLs
- ✅ Updated all templates to use `https://net-worth-tracker.gen3ric-labs.com/static/images/gen3ric-labs-logo.svg`

### 3. CSS Not Applied to Login/Signup Pages
- ✅ Fixed CSS loading by using absolute HTTPS URLs
- ✅ Added missing CSS classes for social login sections
- ✅ Ensured proper static file serving

## Deployment Steps

### 1. Server Setup
```bash
# Install required packages
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx certbot python3-certbot-nginx

# Clone your repository
git clone https://github.com/ericyng/networthtracker.git
cd networthtracker
```

### 2. Python Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Django Configuration
```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 4. SSL Certificate
```bash
# Get SSL certificate from Let's Encrypt
sudo certbot --nginx -d net-worth-tracker.gen3ric-labs.com

# Test certificate renewal
sudo certbot renew --dry-run
```

### 5. Nginx Configuration
```bash
# Copy the nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/networthtracker

# Update the paths in the config file
sudo nano /etc/nginx/sites-available/networthtracker

# Enable the site
sudo ln -s /etc/nginx/sites-available/networthtracker /etc/nginx/sites-enabled/

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

### 6. Django Production Server
```bash
# Run Django with production settings
python manage.py runserver 0.0.0.0:8000 --settings=backend.production_settings

# Or use Gunicorn for production
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 backend.wsgi:application --settings=backend.production_settings
```

### 7. Systemd Service (Optional)
Create `/etc/systemd/system/networthtracker.service`:
```ini
[Unit]
Description=NetWorth Tracker Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/venv/bin"
ExecStart=/path/to/your/project/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 backend.wsgi:application --settings=backend.production_settings
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable networthtracker
sudo systemctl start networthtracker
```

## Environment Variables

Create a `.env` file in your project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=net-worth-tracker.gen3ric-labs.com
DATABASE_URL=your-database-url
```

## File Permissions
```bash
# Set proper permissions
sudo chown -R www-data:www-data /path/to/your/project
sudo chmod -R 755 /path/to/your/project
sudo chmod -R 644 /path/to/your/project/logs/
```

## Monitoring
```bash
# Check application status
sudo systemctl status networthtracker

# Check nginx status
sudo systemctl status nginx

# View logs
sudo journalctl -u networthtracker
sudo tail -f /var/log/nginx/error.log
```

## Troubleshooting

### Static Files Not Loading
1. Check if static files are collected: `ls -la staticfiles/`
2. Verify nginx configuration: `sudo nginx -t`
3. Check file permissions: `ls -la staticfiles/`

### SSL Issues
1. Verify certificate: `sudo certbot certificates`
2. Check nginx SSL configuration
3. Test SSL: `curl -I https://net-worth-tracker.gen3ric-labs.com`

### Django Errors
1. Check Django logs: `tail -f logs/django.log`
2. Verify settings: `python manage.py check --deploy`
3. Test database connection: `python manage.py dbshell`

## Security Checklist

- [ ] HTTPS enabled and working
- [ ] SSL certificate valid and auto-renewing
- [ ] Django DEBUG=False in production
- [ ] Static files served by nginx
- [ ] Proper file permissions set
- [ ] Security headers configured
- [ ] Database properly configured
- [ ] Logs being written and monitored
- [ ] Backup strategy in place

## Support

If you encounter issues:
1. Check the logs in `/var/log/nginx/` and `logs/django.log`
2. Verify all configuration files
3. Test each component individually
4. Check the GitHub issues page for known problems 