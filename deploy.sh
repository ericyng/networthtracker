#!/bin/bash

# NetWorth Tracker Deployment Script

echo "🚀 Starting NetWorth Tracker deployment..."

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create logs directory if it doesn't exist
echo "📝 Creating logs directory..."
mkdir -p logs

# Set proper permissions
echo "🔐 Setting file permissions..."
chmod 755 staticfiles/
chmod 644 logs/

echo "✅ Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Configure your web server (nginx/apache) to serve static files from staticfiles/"
echo "2. Set up SSL certificate for HTTPS"
echo "3. Configure your web server to proxy to Django"
echo "4. Set environment variables for production"
echo ""
echo "🌐 Your site should be accessible at: https://net-worth-tracker.gen3ric-labs.com" 