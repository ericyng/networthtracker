# PickupKids Backend API

Django REST Framework API for the PickupKids coordination app.

## 🚀 Features

### Core API Endpoints
- **Authentication:** JWT-based authentication
- **Families:** Manage family groups and members
- **Children:** Child profiles and information
- **Schedules:** Pickup/dropoff scheduling
- **Locations:** Location management
- **Notifications:** Push notification system
- **Real-time Updates:** WebSocket connections

### Data Models
- **User:** Parent/caregiver accounts
- **Family:** Family groups with multiple adults and children
- **Child:** Child profiles with preferences
- **Schedule:** Pickup/dropoff schedules
- **Location:** Pickup/dropoff locations
- **Notification:** Push notification records

## 🛠️ Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis (for real-time features)

### Installation

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

## 📚 API Documentation

### Authentication
- **POST** `/api/auth/login/` - User login
- **POST** `/api/auth/register/` - User registration
- **POST** `/api/auth/refresh/` - Refresh JWT token

### Families
- **GET** `/api/families/` - List user's families
- **POST** `/api/families/` - Create new family
- **GET** `/api/families/{id}/` - Get family details
- **PUT** `/api/families/{id}/` - Update family
- **DELETE** `/api/families/{id}/` - Delete family

### Children
- **GET** `/api/children/` - List family children
- **POST** `/api/children/` - Add child to family
- **GET** `/api/children/{id}/` - Get child details
- **PUT** `/api/children/{id}/` - Update child
- **DELETE** `/api/children/{id}/` - Remove child

### Schedules
- **GET** `/api/schedules/` - List schedules
- **POST** `/api/schedules/` - Create schedule
- **GET** `/api/schedules/{id}/` - Get schedule details
- **PUT** `/api/schedules/{id}/` - Update schedule
- **DELETE** `/api/schedules/{id}/` - Delete schedule

### Locations
- **GET** `/api/locations/` - List locations
- **POST** `/api/locations/` - Add location
- **GET** `/api/locations/{id}/` - Get location details
- **PUT** `/api/locations/{id}/` - Update location
- **DELETE** `/api/locations/{id}/` - Delete location

## 🔧 Configuration

### Environment Variables
```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@localhost/pickupkids

# Redis
REDIS_URL=redis://localhost:6379/0

# Firebase (Push Notifications)
FIREBASE_CREDENTIALS_PATH=path/to/firebase-credentials.json

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_models.py

# Run with coverage
pytest --cov=.
```

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False`
2. Configure production database
3. Set up Redis for real-time features
4. Configure Firebase for push notifications
5. Set up SSL certificates
6. Configure web server (Nginx + Gunicorn)

### Docker Deployment
```bash
docker-compose up -d
```

## 📝 Development

### Code Style
- **Black** for code formatting
- **Flake8** for linting
- **isort** for import sorting

### Pre-commit Hooks
```bash
pre-commit install
```

## 🔒 Security

- JWT-based authentication
- CORS configuration
- Rate limiting
- Input validation
- SQL injection prevention
- XSS protection 