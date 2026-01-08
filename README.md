# Backend-Automation-System

A **production‑ready FastAPI backend** designed for secure automation workflows. The system includes **JWT‑based authentication**, **PostgreSQL integration**, and is structured for **scalable cloud deployment (AWS‑ready)**.

---

### Current Features
* FastAPI‑based REST APIs
* JWT Bearer authentication
* Modular and clean project structure
* PostgreSQL database support
* OpenAPI / Swagger documentation
* AWS‑friendly deployment architecture

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

## Authentication

This system uses **JWT Bearer Authentication**.

* Clients must pass the token in the header:

```
Authorization: Bearer <access_token>
```

* Token validation is enforced on secured endpoints via dependency injection.

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
