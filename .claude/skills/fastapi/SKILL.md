---
name: fastapi
description: Comprehensive FastAPI development skill for building Python web APIs from simple hello world to production-ready applications. Use when building REST APIs, creating web services, implementing backends, or when the user mentions FastAPI, Python APIs, async Python web frameworks, or needs to build endpoints with automatic documentation, data validation, and type hints.
---

# FastAPI Development Skill

Build FastAPI applications from hello world to production-ready APIs using official documentation patterns.

## Quick Start

### Create New Project

Use the project scaffolding script:

```bash
# Basic project
python scripts/create_project.py my-api

# With Docker support
python scripts/create_project.py my-api --with-docker

# With tests
python scripts/create_project.py my-api --with-tests

# Full stack
python scripts/create_project.py my-api --with-docker --with-tests
```

### Hello World

For the simplest FastAPI app, copy from `assets/hello-world/`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Run with:
```bash
fastapi dev main.py
```

### Production-Ready Template

For a complete production structure, copy from `assets/production-template/`:
- Structured layout (routers, schemas, services)
- Configuration management
- Middleware (CORS, GZip)
- Testing with pytest
- Docker deployment
- Environment variables

## Core Patterns

### Path Operations

Basic HTTP methods and routing:

```python
@app.get("/items/")           # List items
@app.get("/items/{id}")       # Get item
@app.post("/items/")          # Create item
@app.put("/items/{id}")       # Update item
@app.delete("/items/{id}")    # Delete item
```

**See [references/path-operations.md](references/path-operations.md) for:**
- Path parameters with type hints
- Query parameters (required, optional, default values)
- Request body with Pydantic models
- Response models
- Data validation
- Multiple parameter types

### Request/Response Handling

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

FastAPI automatically:
- Validates request data
- Converts types
- Generates API documentation
- Returns proper HTTP responses

### Dependency Injection

Create reusable components:

```python
from typing import Annotated
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
async def read_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()
```

**See [references/dependencies.md](references/dependencies.md) for:**
- Basic dependencies
- Classes as dependencies
- Sub-dependencies
- Dependencies with yield (setup/teardown)
- Global dependencies
- Dependency overrides for testing

## Security and Authentication

FastAPI provides built-in security utilities:

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/me")
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)]):
    return decode_token(token)
```

**See [references/security.md](references/security.md) for:**
- OAuth2 with Password and Bearer
- OAuth2 with JWT tokens (production-ready)
- API Key authentication (header, query, cookie)
- HTTP Basic Auth
- Security best practices
- Password hashing
- Role-based access control

## Middleware and CORS

Add cross-cutting concerns:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**See [references/middleware-cors.md](references/middleware-cors.md) for:**
- Custom middleware
- CORS configuration
- Built-in middleware (GZip, TrustedHost, HTTPS redirect)
- Common patterns (logging, error handling, rate limiting)

## Testing

Use TestClient for easy testing:

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

**See [references/testing.md](references/testing.md) for:**
- TestClient setup
- Testing different request types
- Testing authentication
- Overriding dependencies
- Testing file uploads
- Pytest fixtures and parametrization
- Complete testing examples

## Background Tasks

Run tasks after sending responses:

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email
    pass

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "notification")
    return {"message": "Notification sent in the background"}
```

**See [references/background-tasks.md](references/background-tasks.md) for:**
- Email notifications
- File processing
- Webhooks
- Database cleanup
- Audit logging
- When to use Celery instead

## Production Deployment

Deploy with Uvicorn and Gunicorn:

```bash
# Development
fastapi dev app/main.py

# Production
fastapi run app/main.py --port 8000 --workers 4

# With Gunicorn
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

**See [references/deployment.md](references/deployment.md) for:**
- Production server setup
- Worker configuration
- Docker deployment
- Environment configuration
- HTTPS and reverse proxy
- Performance optimization
- Monitoring and logging
- Systemd service setup

## Project Structure

Recommended structure for production applications:

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Settings
│   ├── routers/             # API routes
│   │   ├── users.py
│   │   └── items.py
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── dependencies/        # Shared dependencies
├── tests/                   # Test suite
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

## Common Workflows

### Building a Simple API

1. Start with hello-world template from `assets/hello-world/`
2. Add path operations in `main.py`
3. Define Pydantic models for validation
4. Add error handling with `HTTPException`
5. Test with interactive docs at `/docs`

### Building a Production API

1. Use `scripts/create_project.py` or copy `assets/production-template/`
2. Configure environment in `.env`
3. Define schemas in `app/schemas/`
4. Create routers in `app/routers/`
5. Add dependencies in `app/dependencies/`
6. Implement business logic in `app/services/`
7. Write tests in `tests/`
8. Deploy with Docker or Gunicorn

### Adding Authentication

1. See [references/security.md](references/security.md) for complete examples
2. For JWT: Install `python-jose` and `passlib`
3. Create OAuth2 scheme and password hashing
4. Implement token creation and validation
5. Add dependency for current user
6. Protect routes with authentication dependency

### Adding Database Integration

1. Install SQLAlchemy: `pip install sqlalchemy`
2. Create database models in `app/models/`
3. Create database dependency with yield:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
4. Use in path operations:
```python
@app.get("/users/")
async def read_users(db: Annotated[Session, Depends(get_db)]):
    return db.query(User).all()
```

### Adding CORS

1. Import and configure middleware (see [references/middleware-cors.md](references/middleware-cors.md))
2. Specify allowed origins (never use `["*"]` with `allow_credentials=True`)
3. Configure allowed methods and headers
4. Test from browser console

## Development Tips

### Auto-Reload During Development

```bash
fastapi dev app/main.py
```

The `fastapi dev` command automatically:
- Enables hot-reload
- Uses port 8000
- Shows detailed error messages
- Enables debug mode

### Interactive API Documentation

FastAPI automatically generates:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

Use Swagger UI to test endpoints directly in the browser.

### Type Hints for Editor Support

Always use type hints for:
- Better editor autocompletion
- Automatic validation
- Auto-generated documentation

```python
# Good
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    pass

# Missing benefits without type hints
@app.get("/items/{item_id}")
async def read_item(item_id, q=None):
    pass
```

### Async vs Sync

Use `async def` when:
- Using `await` (database queries, HTTP requests)
- I/O-bound operations

Use regular `def` when:
- CPU-bound operations
- Blocking libraries

FastAPI handles both correctly.

## Debugging

### Enable Debug Mode

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

### Check Request/Response

```python
from fastapi import Request

@app.get("/debug")
async def debug(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
    }
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

@app.get("/items/")
async def read_items():
    logger.info("Reading items")
    return items
```

## Reference Documentation

For detailed information on specific topics:

- **[path-operations.md](references/path-operations.md)** - Path params, query params, request/response handling
- **[dependencies.md](references/dependencies.md)** - Dependency injection patterns
- **[security.md](references/security.md)** - Authentication and authorization
- **[middleware-cors.md](references/middleware-cors.md)** - Middleware and CORS configuration
- **[testing.md](references/testing.md)** - Testing with TestClient and pytest
- **[background-tasks.md](references/background-tasks.md)** - Background task patterns
- **[deployment.md](references/deployment.md)** - Production deployment guide

## Scripts

- **[scripts/create_project.py](scripts/create_project.py)** - Scaffold new FastAPI projects
- **[scripts/start_dev.sh](scripts/start_dev.sh)** - Start development server

## Assets

- **[assets/hello-world/](assets/hello-world/)** - Minimal FastAPI application
- **[assets/production-template/](assets/production-template/)** - Production-ready project structure

## Key Principles

1. **Type hints everywhere** - Enables validation and documentation
2. **Pydantic for data** - Request/response validation
3. **Dependencies for reuse** - Avoid code repetition
4. **Test with TestClient** - Easy, fast testing
5. **Environment variables** - Never hardcode secrets
6. **Structure matters** - Organize code as it grows
7. **Read the docs** - FastAPI has excellent documentation

## Common Issues

### Import Errors

Ensure proper package structure with `__init__.py` files in all packages.

### CORS Errors

Configure CORS middleware with specific origins, not `["*"]` in production.

### Validation Errors (422)

Check Pydantic models - FastAPI validates request data automatically.

### Database Connection Errors

Use dependencies with `yield` for proper connection management.

### Deployment Issues

- Set `DEBUG=False` in production
- Use multiple workers for production
- Configure proper CORS origins
- Use environment variables for secrets
