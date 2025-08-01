# Net Worth Tracker - Deployment Guide

## Overview

This guide covers deploying the Net Worth Tracker application using Docker and Docker Compose. The application is designed to run in a containerized environment with PostgreSQL, Redis, and Nginx.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- Domain name (for production)
- SSL certificates (for production)

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd networthtracker
```

### 2. Environment Configuration
```bash
cp env.example .env
```

Edit the `.env` file with your configuration:
```bash
# Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://networthtracker:your_secure_password_here@db:5432/networthtracker

# Redis
REDIS_URL=redis://redis:6379/1

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Start the Application
```bash
docker-compose up -d
```

### 4. Access the Application
- Web application: http://localhost:8080
- Admin panel: http://localhost:8080/admin

## Production Deployment

### 1. Production Environment Setup

#### SSL Certificates
Create an `ssl` directory and add your certificates:
```bash
mkdir ssl
# Add your SSL certificates:
# - ssl/cert.pem (certificate)
# - ssl/key.pem (private key)
```

#### Production Docker Compose
Use the production configuration:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 2. Database Setup

#### Initial Migration
```bash
docker-compose exec web python manage.py migrate
```

#### Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

#### Collect Static Files
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### 3. Nginx Configuration

The application includes an Nginx configuration file (`nginx.conf`) that:
- Serves static files
- Proxies requests to the Django application
- Handles SSL termination
- Provides security headers

### 4. Security Considerations

#### Environment Variables
- Use strong, unique passwords
- Generate a secure Django secret key
- Use environment-specific settings

#### Database Security
- Change default PostgreSQL passwords
- Use SSL connections in production
- Regular database backups

#### Application Security
- Keep Django and dependencies updated
- Use HTTPS in production
- Configure proper CORS settings
- Enable security middleware

## Docker Configuration

### Services Overview

#### Web Service (Django)
- **Image:** Built from local Dockerfile
- **Port:** 8000 (internal)
- **Dependencies:** Database, Redis
- **Volumes:** Static files, media files, logs

#### Database Service (PostgreSQL)
- **Image:** postgres:15
- **Port:** 5432 (internal)
- **Volumes:** Persistent data storage
- **Health Check:** Database connectivity

#### Nginx Service
- **Image:** nginx:alpine
- **Ports:** 80, 443 (external)
- **Volumes:** SSL certificates, static files
- **Dependencies:** Web service

#### Redis Service
- **Image:** redis:7-alpine
- **Port:** 6379 (internal)
- **Health Check:** Redis connectivity

### Dockerfile Details

The application Dockerfile:
- Uses Python 3.11 slim image
- Installs system dependencies
- Creates non-root user for security
- Sets up health checks
- Configures proper permissions

### Volume Management

#### Persistent Volumes
- `postgres_data`: Database data
- `static_files`: Static assets
- `media_files`: User uploads

#### Bind Mounts
- `./logs`: Application logs
- `./ssl`: SSL certificates
- `./nginx.conf`: Nginx configuration

## Environment-Specific Configurations

### Development
- Uses SQLite database
- Debug mode enabled
- Local file serving
- Development settings module

### Docker Development
- Uses PostgreSQL
- Debug mode disabled
- Static file collection
- Docker settings module

### Production
- Uses PostgreSQL with SSL
- Debug mode disabled
- CDN-ready static files
- Production settings module
- Security optimizations

## Monitoring and Maintenance

### Health Checks
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx

# Health check endpoints
curl http://localhost:8080/health/
```

### Backup Strategy

#### Database Backups
```bash
# Create backup
docker-compose exec db pg_dump -U networthtracker networthtracker > backup.sql

# Restore backup
docker-compose exec -T db psql -U networthtracker networthtracker < backup.sql
```

#### File Backups
- Static files: `/app/staticfiles/`
- Media files: `/app/media/`
- Logs: `/app/logs/`

### Updates and Maintenance

#### Application Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate
```

#### Dependency Updates
```bash
# Update requirements
pip freeze > requirements.txt

# Rebuild with new dependencies
docker-compose build --no-cache web
docker-compose up -d web
```

## Troubleshooting

### Common Issues

#### Database Connection Errors
- Check database service is running
- Verify environment variables
- Check network connectivity

#### Static Files Not Loading
- Run collectstatic command
- Check Nginx configuration
- Verify volume mounts

#### SSL Certificate Issues
- Check certificate paths
- Verify certificate validity
- Check Nginx SSL configuration

#### Performance Issues
- Monitor resource usage
- Check database queries
- Optimize static file serving
- Review caching configuration

### Debug Commands
```bash
# Check container logs
docker-compose logs [service_name]

# Access container shell
docker-compose exec web bash
docker-compose exec db psql -U networthtracker

# Check network connectivity
docker-compose exec web ping db
docker-compose exec web ping redis

# Monitor resource usage
docker stats
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer for multiple web instances
- Configure shared Redis for sessions
- Use external database service
- Implement CDN for static files

### Performance Optimization
- Database connection pooling
- Redis caching strategy
- Static file optimization
- Database indexing
- Query optimization

## Security Checklist

- [ ] Change default passwords
- [ ] Use HTTPS in production
- [ ] Configure firewall rules
- [ ] Enable security headers
- [ ] Regular security updates
- [ ] Database access controls
- [ ] File permission settings
- [ ] Log monitoring
- [ ] Backup encryption
- [ ] SSL certificate management

## Support and Resources

- Django Documentation: https://docs.djangoproject.com/
- Docker Documentation: https://docs.docker.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Nginx Documentation: https://nginx.org/en/docs/ 