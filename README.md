# Carpool Backend (Django + FastAPI)

A production-ready Python backend for a Carpool application using Django REST Framework and FastAPI.

## 🚀 Quick Start with Docker

```bash
# Start all services
docker-compose up -d

# Services will be available at:
# - Django API: http://localhost:8000
# - FastAPI: http://localhost:8080
# - PostgreSQL: localhost:5432
# - FastAPI Docs: http://localhost:8080/docs
```

## 📋 System Requirements

- Docker & Docker Compose
- Or Python 3.11+ (for local development)

## 🏗️ Architecture

- **Django**: Core REST API with JWT authentication, models, and admin panel
- **FastAPI**: High-performance services, real-time features, and interactive API docs
- **PostgreSQL**: Production-grade database
- **Docker**: Complete containerization for consistent environments

## 🔐 Authentication

All protected endpoints require JWT token:

```bash
# 1. Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_driver",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'

# 2. Get Token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_driver", "password": "SecurePass123!"}'

# 3. Use Token
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:8000/api/users/me/
```

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh expired token

### User Management
- `GET /api/users/me/` - Get current user profile (requires auth)
- `PUT /api/users/me/` - Update profile (requires auth)

### Vehicles
- `GET /api/vehicles/` - List all vehicles
- `POST /api/vehicles/` - Create vehicle (requires auth)
- `GET /api/vehicles/{id}/` - Get vehicle details
- `PUT /api/vehicles/{id}/` - Update vehicle (requires auth)
- `DELETE /api/vehicles/{id}/` - Delete vehicle (requires auth)
- `GET /api/vehicles/my_vehicles/` - List my vehicles (requires auth)

### Rides
- `GET /api/rides/` - List all rides (supports filtering)
- `POST /api/rides/` - Create ride (requires auth)
- `GET /api/rides/{id}/` - Get ride details
- `PUT /api/rides/{id}/` - Update ride (requires auth)
- `DELETE /api/rides/{id}/` - Delete ride (requires auth)
- `GET /api/rides/my_rides/` - List my rides (requires auth)
- `GET /api/rides/{id}/availability/` - Check seat availability

### Bookings
- `GET /api/bookings/` - List my bookings (requires auth)
- `POST /api/bookings/` - Book a ride (requires auth)
- `GET /api/bookings/{id}/` - Get booking details (requires auth)
- `DELETE /api/bookings/{id}/` - Cancel booking (requires auth)
- `POST /api/bookings/{id}/cancel/` - Cancel booking (alternative) (requires auth)

### Query Parameters
- `?origin=Lagos` - Filter rides by origin
- `?destination=Ibadan` - Filter rides by destination
- `?available_only=true` - Show only available rides
- `?page=2` - Pagination
- `?page_size=20` - Custom page size

## 🛠️ Local Development (Without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
cd carpool_django
python manage.py migrate

# Start Django
python manage.py runserver

# In another terminal, start FastAPI
cd ..
uvicorn fastapi_app.main:app --reload
```

## 📊 Database Models

### User
- Custom user model with phone number
- Extends Django's AbstractUser

### Vehicle
- Owner (ForeignKey to User)
- Make, Model, Plate Number
- Number of seats

### Ride
- Driver (ForeignKey to User)
- Vehicle (ForeignKey to Vehicle)
- Origin, Destination
- Departure time, Available seats
- Price (in cents)

### Booking
- Ride (ForeignKey to Ride)
- Passenger (ForeignKey to User)
- Number of seats booked
- Created timestamp

## ✨ Features

- ✅ User registration with password validation
- ✅ JWT-based authentication
- ✅ Complete CRUD operations
- ✅ Ride search and filtering
- ✅ Real-time seat availability tracking
- ✅ Booking system with validation
- ✅ User profile with statistics
- ✅ Pagination support
- ✅ Permission-based access control
- ✅ Comprehensive error handling
- ✅ CORS enabled for frontend integration
- ✅ Interactive API documentation (Swagger/OpenAPI)

## 🔒 Security Notes

For production deployment:
1. Set `CARPOOL_SECRET_KEY` environment variable to a strong secret
2. Set `DEBUG=False` in Django settings
3. Configure allowed hosts
4. Use HTTPS only
5. Implement rate limiting
6. Add request logging and monitoring

## 📝 Configuration

Environment variables (set in docker-compose.yml or .env):
- `CARPOOL_SECRET_KEY` - JWT signing key (default: dev secret)
- `POSTGRES_DB` - Database name (default: carpool)
- `POSTGRES_USER` - Database user (default: carpool_user)
- `POSTGRES_PASSWORD` - Database password (default: carpool_password)
- `POSTGRES_HOST` - Database host (default: db)
- `POSTGRES_PORT` - Database port (default: 5432)

## 🧪 Testing

### Interactive API Testing
- Django REST Framework Browsable API: http://localhost:8000/api/
- FastAPI Swagger UI: http://localhost:8080/docs
- FastAPI ReDoc: http://localhost:8080/redoc

### Database Access
```bash
# Connect to PostgreSQL
psql -h localhost -U carpool_user -d carpool -W
# Password: carpool_password
```

## 📦 Deployment

This application is containerized and ready for deployment:

```bash
# Build for production
docker-compose build

# Deploy (configure ports, volumes, and secrets first)
docker-compose up -d
```

## 📄 License

This project is part of the Carpool App suite.
