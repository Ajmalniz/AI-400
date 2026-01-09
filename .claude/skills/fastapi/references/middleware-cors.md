# Middleware and CORS Reference

Complete guide to implementing middleware and configuring CORS in FastAPI applications.

## Table of Contents
- Custom Middleware
- CORS Configuration
- Built-in Middleware
- Common Middleware Patterns

## Custom Middleware

Middleware processes every request before path operations and every response before returning.

### Basic Middleware Structure

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

**Parameters:**
- `request`: The incoming HTTP request
- `call_next`: Function that passes the request to the next middleware/path operation

**Execution flow:**
1. Code before `await call_next(request)` runs before the path operation
2. Path operation executes
3. Code after `await call_next(request)` runs after the path operation

### Multiple Middleware Execution Order

When using `app.add_middleware()`, the last added is outermost:

```python
from starlette.middleware.base import BaseHTTPMiddleware

class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Custom-Header"] = "Custom Value"
        return response

app.add_middleware(CustomHeaderMiddleware)
app.add_middleware(AnotherMiddleware)

# Execution:
# Request:  AnotherMiddleware -> CustomHeaderMiddleware -> route handler
# Response: route handler -> CustomHeaderMiddleware -> AnotherMiddleware
```

## CORS Configuration

CORS (Cross-Origin Resource Sharing) allows frontend apps from different origins to access your API.

### What is an Origin?

An origin = protocol + domain + port

**Different origins:**
- `http://localhost` (default port 80)
- `https://localhost` (different protocol)
- `http://localhost:8080` (different port)

### Basic CORS Setup

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "https://myapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "Hello World"}
```

### CORS Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `allow_origins` | List of allowed origins or `['*']` for any | Required |
| `allow_origin_regex` | Regex pattern for allowed origins | `None` |
| `allow_methods` | List of HTTP methods or `['*']` | `['GET']` |
| `allow_headers` | List of allowed headers or `['*']` | `[]` |
| `allow_credentials` | Enable cookies for cross-origin requests | `False` |
| `expose_headers` | Response headers accessible to browser | `[]` |
| `max_age` | Cache time in seconds for CORS responses | `600` |

### Allow All Origins (Development Only)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Warning:** Don't use `allow_origins=["*"]` with `allow_credentials=True` in production!

### Regex Pattern for Origins

```python
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex='https://.*\.example\.org',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This allows:
- `https://app.example.org`
- `https://api.example.org`
- `https://staging.example.org`

### Production CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myapp.com",
        "https://www.myapp.com",
        "https://app.myapp.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Total-Count", "X-Page-Size"],
    max_age=3600,
)
```

## Built-in Middleware

### TrustedHostMiddleware

Protect against Host header attacks:

```python
from fastapi.middleware.trustedhosts import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)
```

### GZipMiddleware

Compress responses:

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

Compresses responses larger than 1000 bytes.

### HTTPSRedirectMiddleware

Redirect HTTP to HTTPS:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app.add_middleware(HTTPSRedirectMiddleware)
```

## Common Middleware Patterns

### Request Logging

```python
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

### Error Handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
```

### Request ID Tracking

```python
import uuid
from fastapi import Request

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
```

Access request ID in path operations:

```python
@app.get("/items/")
async def read_items(request: Request):
    request_id = request.state.request_id
    return {"request_id": request_id}
```

### Authentication Middleware

```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        if request.url.path in ["/", "/health", "/docs", "/openapi.json"]:
            return await call_next(request)

        # Check auth header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing or invalid authorization header"}
            )

        token = auth_header.split(" ")[1]
        # Validate token...

        return await call_next(request)

app.add_middleware(AuthMiddleware)
```

### Rate Limiting

```python
import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 10, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host

        # Clean old requests
        now = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < self.period
        ]

        # Check rate limit
        if len(self.requests[client_ip]) >= self.calls:
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded"}
            )

        # Add current request
        self.requests[client_ip].append(now)

        return await call_next(request)

app.add_middleware(RateLimitMiddleware, calls=10, period=60)
```

### Response Time Tracking

```python
import time
from fastapi import Request

@app.middleware("http")
async def track_response_time(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time

    # Log slow requests
    if process_time > 1.0:  # More than 1 second
        logger.warning(
            f"Slow request: {request.method} {request.url} took {process_time:.2f}s"
        )

    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Database Session Middleware

```python
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.db = SessionLocal()
        try:
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

app.add_middleware(DBSessionMiddleware)

# Access in path operations
@app.get("/users/")
async def read_users(request: Request):
    db = request.state.db
    users = db.query(User).all()
    return users
```

### Security Headers

```python
from fastapi import Request

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

## Important Notes

### Middleware vs Dependencies

- **Middleware**: Runs for every request, including 404s
- **Dependencies**: Run only for matching path operations

### Background Tasks and Middleware

Background tasks run **after** all middleware has completed.

### Exception Handling

Use exception handlers for specific exceptions instead of try/except in middleware:

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

## Key Points

- Middleware processes every request before path operations
- Use `@app.middleware("http")` for simple middleware
- Use `BaseHTTPMiddleware` for class-based middleware
- CORS is required for frontend apps on different origins
- Never use `allow_origins=["*"]` with `allow_credentials=True`
- Middleware executes in reverse order of addition
- Background tasks run after all middleware
- Use timing-safe operations for authentication
- Consider using dependencies instead of middleware for path-specific logic
