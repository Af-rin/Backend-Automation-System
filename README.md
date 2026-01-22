# Backend-Automation-System

A **production‑ready FastAPI backend** designed for secure automation workflows. The system includes **JWT‑based authentication**, **PostgreSQL integration**, and is structured for **scalable cloud deployment (AWS‑ready)**.

---

### Current Features
* FastAPI‑based REST APIs
* JWT Bearer authentication
* Role-based access control (Admin/User)
* Modular and clean project structure
* PostgreSQL database support
* OpenAPI / Swagger documentation
* AWS‑friendly deployment architecture
* Automated API tests with pytest

---

## Tech Stack

* **Backend Framework:** FastAPI
* **Language:** Python 3.10+
* **Authentication:** JWT (Bearer Token)
* **Database:** PostgreSQL (via SQLAlchemy)
* **API Spec:** OpenAPI 3.1
* **Deployment:** Docker / AWS (ECS, EC2, or Lambda‑ready)

---

## Project Structure (High-level)

```text

app/
├── api/            # Routes & controllers
├── models/         # Database models
├── services/       # Business logic
├── middlewares/    # Auth, logging, limits
├── utils/          # JWT, encryption, helpers, enums
├── core/           # Config & logging
└── db/             # Database connection

```

---

## Authentication & Authorization Flow

This system implements **JWT-based authentication with role-based authorization**.

### Workflow
1. Client sends credentials to `/api/v1/auth/login`
2. Server validates the user against PostgreSQL
3. On successful authentication:
   - A JWT access token is generated
   - Token payload includes user_id, role and expiry
4. Client sends the token in every request using:
```
Authorization: Bearer <access_token>
```
5. Protected endpoints validate the token on each request
6. Middleware validates:
  * Token existence
  * Token signature
  * Token expiration
7. Role-based access is enforced at route level

### Example
* ADMIN → can access /auth/getUsers
* USER → forbidden (`403`)

---

### Request Lifecycle
1. Incoming request reaches FastAPI router
2. Authentication middleware validates JWT (for secured routes)
3. Dependencies inject:
   - Database session
   - Current authenticated user
4. Business logic is executed
5. Structured JSON response is returned

---

## Design Decisions
- **JWT Authentication:** Stateless authentication suitable for scalable and distributed systems
- **Dependency Injection:** Used for database sessions and authentication to keep routes clean and testable
- **Role-Based Access Control:** Admin-only routes enforced at dependency level
- **Pagination:** Implemented to prevent large payloads and improve endpoint performance

---

## Available API Endpoints

### 1 Health Check

**GET** `/api/v1/health`

* Used for service monitoring
* Requires Bearer authentication

**Response**

```json
{
  "status": "ok"
}
```

---

### 2 Login

**POST** `/api/v1/auth/login`

Authenticate a user and generate a JWT token.

**Request Body**

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Successful Response**

```json
{
  "error": false,
  "data": {
    "access_token": "jwt_token",
    "token_type": "bearer",
    "expires_in_utc": "2026-01-07T10:30:00Z"
  }
}
```

---

### 3 Get Users

**GET** `/api/v1/auth/getUsers`

Retrieve a list of users.

* Secured endpoint - only admin can access
* Requires valid JWT

**Response**

```json
{
  "error": false,
  "data": {
    "users": [],
    "message": "Users retrieved successfully"
  }
}
```

---

## Testing Strategy

This project includes **automated API tests** using ```pytest``` to ensure correctness, security, and authorization behavior.
- Fixtures are used to manage:
  - Test database sessions
  - Admin and non-admin users

### What is covered
  * Login success flow
  * Invalid credentials handling
  * Missing payload validation
  * JWT token generation
  * Admin-only access enforcement
  * Unauthorized & invalid token handling
  * Pagination validation with consistent response metadata
  * Boundary condition handling for empty result sets

### Test Structure
```
test/
├── conftest.py
├── test_auth.py
```

### Sample Scenarios Covered
  * Successful admin login returns JWT
  * Invalid password returns ```401```
  * Missing login payload returns ```400```
  * Non-admin user accessing admin route returns ```403```
  * Invalid or missing JWT returns ```401```

### Example (Login Test)
```
def test_login_success(client, admin_user):
    payload = {
        "username": "admin",
        "email": admin_user.email,
        "password": "admin123"
    }

    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json()["data"]
```
### Running Tests Locally
```
pytest
```
or
```
pytest -v
```

All tests run against an isolated test database using fixtures.

---

## API Documentation

Interactive API documentation is available at:

* **Swagger UI:** `/docs`
* **ReDoc:** `/redoc`

The API follows **OpenAPI 3.1.0** specifications.

---

## Environment Setup

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

---

## Running the Application

### Local Development

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

The server will start at:

```
http://localhost:5000
```

---

## Docker Support

```bash
docker build -t backend-automation-system .
docker run -p 5000:5000 backend-automation-system
```

---

## Security Notes

* All protected endpoints require JWT authentication
* Token payload is validated on every request
* Unauthorized access returns `401 / 403` appropriately
* Role-based authorization enforced at route level
* Invalid, expired, or missing tokens return appropriate HTTP errors
* Admin-only routes protected via dependency injection

---

## Production Considerations

- Secrets managed via environment variables
- JWT expiry enforced on access tokens
- Designed to run behind an API Gateway / Load Balancer
- Architecture allows future extension with:
  - Refresh tokens
  - Rate limiting
  - Audit logging
  
---

## Future Enhancements

* Role‑based access control (RBAC)
* Refresh token support
* Rate limiting & throttling
* Advanced audit logging

---

## Maintainer

**Af‑rin**
GitHub: [https://github.com/Af-rin](https://github.com/Af-rin)

---

## License

This project is licensed under the **MIT License**.

---
