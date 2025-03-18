# FastAPI python microservice


# Microservice Documentation

## 1. Introduction

Welcome to the **Microservice Template** built with FastAPI! This template showcases:

- **Basic Project Structure**: Clean separation of concerns (main entry point, endpoints, configurations, and security).
- **Authentication**: An example using JWT tokens.
- **External API Calls**: Demonstrates making requests to third-party or internal services.
- **Logging**: Basic logging configuration for startup and shutdown events.
- **Configuration**: Easily manage environment variables for different environments (development, production, etc.).

This documentation will walk you through the structure of the project, how requests are handled, and how the authentication/authorization works.

---

## 2. Architecture at a Glance

```
my_microservice/
│
├── main.py                   # Application entry point
├── app/
│   ├── config.py             # Central configuration (env variables, etc.)
│   ├── logging_conf.py       # Logging setup
│   ├── security/
│   │   ├── __init__.py
│   │   └── jwt.py            # JWT-related functions and dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── auth.py           # Auth-related Pydantic models
│   │   ├── user.py           # User-related Pydantic models
│   │   └── external.py       # External service Pydantic models
│   └── endpoints/
│       ├── __init__.py
│       ├── public.py         # Public endpoints that do not require authentication
│       ├── private.py        # Endpoints that require JWT-based auth
│       ├── auth.py           # Login and token generation endpoints
│       └── external.py       # Demonstrates making HTTP calls to an external API
└── requirements.txt          # Python dependencies
```

### Key Principles

- **Separation of Concerns**: Each endpoint group (public, private, auth, external) lives in its own file under `app/endpoints`.
- **Reusable Modules**: Security utilities, logging configuration, and environment configuration are each in dedicated modules.
- **Pydantic Models**: Inputs and outputs use Pydantic for validation, ensuring predictable data structures and automatically generated OpenAPI docs.

---

## 3. Installation and Setup

### Clone the repository:

```bash
git clone https://github.com/your-org/my_microservice.git
cd my_microservice
```

### Create and activate a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# Windows users:
venv\Scripts\activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the application:

```bash
uvicorn main:app --reload
```

This will start the server in development mode on [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Open API Docs:

Once the server is running, navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the auto-generated interactive documentation.

---

## 4. Main Application Entry Point (`main.py`)



### Explanation:

- `app = FastAPI(...)`: Initializes the FastAPI application.
- **Routers**: Each router (public, private, auth, external) is defined in a dedicated Python file and included here with a unique prefix (`/api/v1/...`).
- **Logging**: On startup/shutdown, the service logs messages indicating the environment or any other important info.
- **CORS**: Allows cross-origin requests; adjust to fit your production security policy.

---

## 5. Configuration (`app/config.py`)



### Key Points:

- `BaseSettings` from Pydantic automatically reads environment variables and `.env` file values.
- `settings` is an instance you can import across the entire application (`settings.ENVIRONMENT`, etc.).

---

## 6. Logging Configuration (`app/logging_conf.py`)



## 7. Security (JWT) (`app/security/jwt.py`)



## 8. Models (`app/models/*`)

### Example: `user.py`

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: Optional[str] = None
```

### Why Pydantic?

- Ensures the data structure is validated against the expected schema.
- Auto-generates OpenAPI docs (which you can see at `/docs`).

---


## 9. Endpoint Implementations (`app/endpoints/*`)

Each file defines a separate `APIRouter` instance that is mounted in `main.py`. The endpoints are structured as follows:

- **Public Endpoints**: Accessible without authentication, such as a welcome message or public user info.
- **Private Endpoints**: Require JWT-based authentication and allow user-specific actions.
- **Auth Endpoints**: Handle login and token generation, providing access control.
- **External API Calls**: Demonstrate how to make HTTP requests to third-party services while ensuring error handling and response validation.

### Key Considerations:

- **Security**: Private endpoints use dependency injection to validate JWT tokens before granting access.
- **Structured API Design**: Each endpoint type is organized in separate files for maintainability.
- **Error Handling**: Proper exception handling ensures that HTTP errors are returned when external requests fail.

This structure ensures a scalable and modular approach to handling different API functionalities.

### Example Implementation of Routers

Below is an example of how routers are implemented and included in `main.py`:

#### `app/endpoints/public.py`
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=dict)
def root_public_endpoint():
    """
    Public endpoint with no authentication required.
    """
    return {"message": "Welcome to the public endpoint!"}
```

#### `main.py`
```python
from fastapi import FastAPI
from app.endpoints.public import router as public_router
from app.endpoints.private import router as private_router
from app.endpoints.auth import router as auth_router
from app.endpoints.external import router as external_router

app = FastAPI()

app.include_router(public_router, prefix="/api/v1/public", tags=["Public Endpoints"])
app.include_router(private_router, prefix="/api/v1/private", tags=["Private Endpoints"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(external_router, prefix="/api/v1/external", tags=["External"])
```

This demonstrates how routers are structured and integrated into the FastAPI application to ensure modular and maintainable API design.