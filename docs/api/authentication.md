# Authentication API

## Endpoints

### Register User
**POST** `/api/auth/register`

Request:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "secure_password"
}
```

Response:
```json
{
  "message": "User created successfully",
  "id": "user-id"
}
```

### Login
**POST** `/api/auth/login`

Request:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "jwt_token",
  "user": {
    "id": "user-id",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Get Profile
**GET** `/api/auth/profile`

Headers:
```
Authorization: Bearer <jwt_token>
```

Response:
```json
{
  "id": "user-id",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user"
}
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

Token lifetime: 24 hours

## Error Responses

```json
{
  "message": "Invalid credentials",
  "statusCode": 401
}
```

Common status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Server Error
