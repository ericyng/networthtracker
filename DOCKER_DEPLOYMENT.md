# Docker Deployment Guide for NetWorth Tracker

## Overview

This guide will help you deploy the NetWorth Tracker application using Docker and Docker Compose. The setup includes:

- **Django Application** - The main web application
- **PostgreSQL Database** - For data storage
- **Redis** - For caching and sessions
- **Nginx** - Reverse proxy and static file serving

## Prerequisites

- Docker installed on your server
- Docker Compose installed
- Domain name pointing to your server
- SSL certificate (optional for development)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ericyng/networthtracker.git
cd networthtracker
```

### 2. Set Up Environment Variables

```bash
# Copy the environment template
cp env.example .env

# Edit the environment file
nano .env
```

**Important variables to update:**
- `SECRET_KEY` - Generate a secure secret key
- `DATABASE_URL` - Update with your database credentials
- `ALLOWED_HOSTS` - Add your domain name
- Email settings if you want email functionality

### 3. Generate a Secure Secret Key

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Build and Start the Application

```bash
# Build the Docker images
docker-compose build

# Start all services
docker-compose up -d

# Check the status
docker-compose ps
```

### 5. Run Database Migrations

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create a superuser (optional)
docker-compose exec web python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

## Production Deployment

### 1. Update Environment Variables for Production

```bash
# Edit .env file
nano .env
```

**Production settings:**
```env
DEBUG=False
SECRET_KEY=your-generated-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECURE_SSL_REDIRECT=True
```

### 2. Set Up SSL Certificate

**Option A: Using Certbot with Docker**

```bash
# Stop nginx temporarily
docker-compose stop nginx

# Run certbot
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to the ssl directory
sudo mkdir -p ssl
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/
sudo chown -R $USER:$USER ssl/

# Start nginx again
docker-compose up -d nginx
```

**Option B: Using Let's Encrypt with Docker**

```bash
# Add certbot service to docker-compose.yml
# (See docker-compose.ssl.yml for example)
```

### 3. Update Nginx Configuration

Edit `nginx.conf` to include SSL:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    
    # ... rest of configuration
}
```

### 4. Deploy

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate
```

## Management Commands

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs web
docker-compose logs nginx
docker-compose logs db

# Follow logs
docker-compose logs -f web
```

### Database Operations

```bash
# Access database shell
docker-compose exec db psql -U networthtracker -d networthtracker

# Create database backup
docker-compose exec db pg_dump -U networthtracker networthtracker > backup.sql

# Restore database
docker-compose exec -T db psql -U networthtracker -d networthtracker < backup.sql
```

### Django Management Commands

```bash
# Run any Django command
docker-compose exec web python manage.py [command]

# Examples:
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py shell
```

### Service Management

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Restart specific service
docker-compose restart web

# Scale services
docker-compose up -d --scale web=3
```

## Monitoring and Maintenance

### Health Checks

```bash
# Check service health
docker-compose ps

# Check application health
curl http://localhost/health/
```

### Backup Strategy

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Database backup
docker-compose exec -T db pg_dump -U networthtracker networthtracker > $BACKUP_DIR/db_$DATE.sql

# Static files backup
tar -czf $BACKUP_DIR/static_$DATE.tar.gz staticfiles/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Log Rotation

Add to your server's logrotate configuration:

```
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
```

## Troubleshooting

### Common Issues

**1. Database Connection Errors**
```bash
# Check database status
docker-compose exec db pg_isready -U networthtracker

# Check database logs
docker-compose logs db
```

**2. Static Files Not Loading**
```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check nginx configuration
docker-compose exec nginx nginx -t
```

**3. SSL Certificate Issues**
```bash
# Check certificate validity
openssl x509 -in ssl/fullchain.pem -text -noout

# Renew certificate
sudo certbot renew
```

**4. Memory Issues**
```bash
# Check resource usage
docker stats

# Increase memory limits in docker-compose.yml
```

### Performance Optimization

**1. Enable Gzip Compression**
Add to nginx.conf:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript;
```

**2. Database Optimization**
```bash
# Analyze database performance
docker-compose exec web python manage.py dbshell
```

**3. Redis Caching**
The application is already configured to use Redis for caching and sessions.

## Security Considerations

1. **Change default passwords** in `.env`
2. **Use strong secret keys**
3. **Keep Docker images updated**
4. **Regular security updates**
5. **Monitor logs for suspicious activity**
6. **Use HTTPS in production**
7. **Implement rate limiting**

## Scaling

### Horizontal Scaling

```bash
# Scale web workers
docker-compose up -d --scale web=3

# Use load balancer
# Add nginx load balancer configuration
```

### Vertical Scaling

Update `docker-compose.yml`:
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
```

## Support

For issues and questions:
1. Check the logs: `docker-compose logs`
2. Review this documentation
3. Check GitHub issues
4. Create a new issue with detailed information 