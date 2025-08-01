# PickupKids API Design

## Overview

The PickupKids API is a RESTful service built with Django REST Framework that provides endpoints for managing family coordination, scheduling, and notifications.

## Base URL
```
https://api.pickupkids.com/v1/
```

## Authentication

All API requests require authentication using JWT tokens.

### Headers
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Core Endpoints

### Authentication

#### POST /auth/login/
Login with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

#### POST /auth/register/
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### POST /auth/refresh/
Refresh access token.

**Request:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Families

#### GET /families/
Get all families for the authenticated user.

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "name": "Smith Family",
      "created_at": "2023-01-01T00:00:00Z",
      "members": [
        {
          "id": 1,
          "user": {
            "id": 1,
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Smith"
          },
          "role": "parent"
        }
      ]
    }
  ]
}
```

#### POST /families/
Create a new family.

**Request:**
```json
{
  "name": "Smith Family"
}
```

#### GET /families/{id}/
Get family details.

#### PUT /families/{id}/
Update family information.

#### DELETE /families/{id}/
Delete family.

### Children

#### GET /children/
Get all children for the authenticated user's families.

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "Emma Smith",
      "age": 8,
      "family": 1,
      "preferences": {
        "favorite_color": "blue",
        "allergies": ["nuts"]
      },
      "photo_url": "https://example.com/photo.jpg"
    }
  ]
}
```

#### POST /children/
Add a child to a family.

**Request:**
```json
{
  "name": "Emma Smith",
  "age": 8,
  "family": 1,
  "preferences": {
    "favorite_color": "blue",
    "allergies": ["nuts"]
  }
}
```

#### GET /children/{id}/
Get child details.

#### PUT /children/{id}/
Update child information.

#### DELETE /children/{id}/
Remove child from family.

### Schedules

#### GET /schedules/
Get all schedules for the authenticated user's families.

**Query Parameters:**
- `date_from`: Filter schedules from this date (YYYY-MM-DD)
- `date_to`: Filter schedules to this date (YYYY-MM-DD)
- `child`: Filter by child ID
- `family`: Filter by family ID

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "child": {
        "id": 1,
        "name": "Emma Smith"
      },
      "type": "pickup",
      "date": "2023-12-01",
      "time": "15:30:00",
      "location": {
        "id": 1,
        "name": "School",
        "address": "123 Main St",
        "coordinates": {
          "lat": 40.7128,
          "lng": -74.0060
        }
      },
      "assigned_to": {
        "id": 1,
        "first_name": "John",
        "last_name": "Smith"
      },
      "status": "confirmed",
      "notes": "Pick up from soccer practice"
    }
  ]
}
```

#### POST /schedules/
Create a new schedule.

**Request:**
```json
{
  "child": 1,
  "type": "pickup",
  "date": "2023-12-01",
  "time": "15:30:00",
  "location": 1,
  "assigned_to": 1,
  "notes": "Pick up from soccer practice"
}
```

#### GET /schedules/{id}/
Get schedule details.

#### PUT /schedules/{id}/
Update schedule.

#### DELETE /schedules/{id}/
Delete schedule.

### Locations

#### GET /locations/
Get all locations for the authenticated user's families.

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "School",
      "address": "123 Main St",
      "coordinates": {
        "lat": 40.7128,
        "lng": -74.0060
      },
      "is_favorite": true,
      "family": 1
    }
  ]
}
```

#### POST /locations/
Add a new location.

**Request:**
```json
{
  "name": "School",
  "address": "123 Main St",
  "coordinates": {
    "lat": 40.7128,
    "lng": -74.0060
  },
  "family": 1
}
```

#### GET /locations/{id}/
Get location details.

#### PUT /locations/{id}/
Update location.

#### DELETE /locations/{id}/
Delete location.

### Notifications

#### GET /notifications/
Get user notifications.

**Query Parameters:**
- `unread_only`: Filter unread notifications only
- `type`: Filter by notification type

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "type": "schedule_reminder",
      "title": "Pickup Reminder",
      "message": "Emma's pickup is in 30 minutes",
      "data": {
        "schedule_id": 1,
        "child_name": "Emma"
      },
      "is_read": false,
      "created_at": "2023-12-01T15:00:00Z"
    }
  ]
}
```

#### POST /notifications/{id}/mark-read/
Mark notification as read.

#### POST /notifications/mark-all-read/
Mark all notifications as read.

### Real-time Updates

#### WebSocket Connection
```
wss://api.pickupkids.com/ws/
```

**Authentication:**
Send JWT token in query parameter:
```
wss://api.pickupkids.com/ws/?token=<access_token>
```

**Message Types:**
- `schedule_update`: Schedule has been updated
- `notification`: New notification received
- `location_update`: Family member location updated

## Error Handling

### Error Response Format
```json
{
  "error": "error_code",
  "message": "Human readable error message",
  "details": {
    "field": "Specific field error"
  }
}
```

### Common Error Codes
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

## Rate Limiting

- **Authentication endpoints:** 5 requests per minute
- **General endpoints:** 100 requests per minute
- **WebSocket connections:** 10 connections per user

## Pagination

List endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Response:**
```json
{
  "count": 100,
  "next": "https://api.pickupkids.com/v1/schedules/?page=2",
  "previous": null,
  "results": [...]
}
```

## Filtering and Sorting

### Filtering
Most list endpoints support filtering by related fields:
```
GET /schedules/?child=1&date_from=2023-12-01
```

### Sorting
Sort by any field with `ordering` parameter:
```
GET /schedules/?ordering=-date,time
```

## Webhooks

### Available Webhooks
- `schedule.created`: New schedule created
- `schedule.updated`: Schedule updated
- `schedule.deleted`: Schedule deleted
- `notification.sent`: Notification sent

### Webhook Payload
```json
{
  "event": "schedule.created",
  "timestamp": "2023-12-01T15:00:00Z",
  "data": {
    "schedule_id": 1,
    "child_name": "Emma",
    "date": "2023-12-01"
  }
}
``` 