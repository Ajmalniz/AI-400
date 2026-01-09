# Testing Reference

Complete guide to testing FastAPI applications with TestClient and pytest.

## Table of Contents
- Setup and Installation
- Basic Testing with TestClient
- Testing Different Request Types
- Testing Authentication
- Testing Dependencies
- Testing File Uploads
- Testing WebSockets
- Async Tests
- Test Organization

## Setup and Installation

### Install Testing Dependencies

```bash
pip install pytest httpx
```

### Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── routers/
│       └── items.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_items.py
├── pytest.ini
└── requirements.txt
```

### pytest.ini Configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

## Basic Testing with TestClient

### Simple Test

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```

**Key points:**
- Use regular `def`, not `async def`
- Use regular calls, not `await`
- TestClient follows pytest conventions

### Testing with Separate Files

**app/main.py:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**tests/test_main.py:**
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
```

## Testing Different Request Types

### GET Requests

```python
def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "name": "Item 1"}

def test_get_with_query_params():
    response = client.get("/items/?skip=0&limit=10")
    assert response.status_code == 200
    assert len(response.json()) <= 10
```

### POST Requests

```python
def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": 45.2}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Foo"
    assert response.json()["price"] == 45.2
```

### PUT Requests

```python
def test_update_item():
    response = client.put(
        "/items/1",
        json={"name": "Updated Item", "price": 99.9}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Item"
```

### DELETE Requests

```python
def test_delete_item():
    response = client.delete("/items/1")
    assert response.status_code == 204

def test_delete_nonexistent_item():
    response = client.delete("/items/999")
    assert response.status_code == 404
```

### Testing with Headers

```python
def test_with_custom_header():
    response = client.get(
        "/items/",
        headers={"X-Token": "test-token"}
    )
    assert response.status_code == 200
```

### Testing with Cookies

```python
def test_with_cookies():
    response = client.get(
        "/items/",
        cookies={"session_id": "abc123"}
    )
    assert response.status_code == 200
```

## Testing Authentication

### Testing Protected Endpoints

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient

app = FastAPI()
security = HTTPBearer()

@app.get("/protected")
async def protected_route(token: str = Depends(security)):
    return {"message": "Access granted"}

client = TestClient(app)

def test_protected_without_auth():
    response = client.get("/protected")
    assert response.status_code == 403

def test_protected_with_auth():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 200
```

### Testing OAuth2 Login

```python
def test_login():
    response = client.post(
        "/token",
        data={
            "username": "johndoe",
            "password": "secret"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post(
        "/token",
        data={
            "username": "wrong",
            "password": "wrong"
        }
    )
    assert response.status_code == 401
```

### Testing with Valid Token

```python
def test_read_current_user():
    # First, get a token
    login_response = client.post(
        "/token",
        data={"username": "johndoe", "password": "secret"}
    )
    token = login_response.json()["access_token"]

    # Then use it
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"
```

## Testing Dependencies

### Overriding Dependencies

```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

async def get_db():
    # Real database connection
    return {"db": "real"}

@app.get("/items/")
async def read_items(db: dict = Depends(get_db)):
    return {"db": db}

# Test with mock database
def override_get_db():
    return {"db": "test"}

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_items():
    response = client.get("/items/")
    assert response.json() == {"db": {"db": "test"}}
```

### Fixture for Dependency Override

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db

@pytest.fixture
def test_db():
    # Setup test database
    return {"db": "test"}

@pytest.fixture
def client(test_db):
    def override_get_db():
        return test_db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_read_items(client):
    response = client.get("/items/")
    assert response.status_code == 200
```

## Testing File Uploads

### Single File Upload

```python
def test_upload_file():
    files = {"file": ("test.txt", b"file content", "text/plain")}
    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"
```

### Multiple File Uploads

```python
def test_upload_multiple_files():
    files = [
        ("files", ("test1.txt", b"content 1", "text/plain")),
        ("files", ("test2.txt", b"content 2", "text/plain")),
    ]
    response = client.post("/uploadfiles/", files=files)
    assert response.status_code == 200
    assert len(response.json()["filenames"]) == 2
```

### File Upload with Form Data

```python
def test_upload_with_form():
    files = {"file": ("test.txt", b"content", "text/plain")}
    data = {"description": "Test file"}
    response = client.post("/upload/", files=files, data=data)
    assert response.status_code == 200
```

## Testing Error Cases

### Testing 404 Errors

```python
def test_read_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
```

### Testing Validation Errors

```python
def test_create_item_invalid_data():
    response = client.post(
        "/items/",
        json={"name": "Test"}  # Missing required "price"
    )
    assert response.status_code == 422  # Unprocessable Entity
    assert "detail" in response.json()
```

### Testing Duplicate Items

```python
def test_create_duplicate_item():
    # Create first item
    client.post("/items/", json={"id": "foo", "name": "Foo"})

    # Try to create duplicate
    response = client.post("/items/", json={"id": "foo", "name": "Foo"})
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
```

## Test Organization Patterns

### Using pytest Fixtures

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_item():
    return {"name": "Test Item", "price": 10.5}

def test_create_item(client, sample_item):
    response = client.post("/items/", json=sample_item)
    assert response.status_code == 201
```

### Setup and Teardown

```python
import pytest

@pytest.fixture(scope="function")
def test_data():
    # Setup: Create test data
    data = {"test": "data"}
    yield data
    # Teardown: Clean up
    # data.clear()

def test_with_setup(test_data):
    assert test_data["test"] == "data"
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("item_id,expected", [
    (1, 200),
    (2, 200),
    (999, 404),
])
def test_get_item(client, item_id, expected):
    response = client.get(f"/items/{item_id}")
    assert response.status_code == expected
```

### Test Classes

```python
class TestItems:
    def test_create_item(self, client):
        response = client.post("/items/", json={"name": "Test"})
        assert response.status_code == 201

    def test_read_items(self, client):
        response = client.get("/items/")
        assert response.status_code == 200

    def test_update_item(self, client):
        response = client.put("/items/1", json={"name": "Updated"})
        assert response.status_code == 200
```

## Async Tests

For async operations outside TestClient:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
```

## Complete Testing Example

**app/main.py:**
```python
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

fake_db = {}

class Item(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str, x_token: Annotated[str, Header()]):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid X-Token")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item, x_token: Annotated[str, Header()]):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid X-Token")
    if item.name in fake_db:
        raise HTTPException(status_code=409, detail="Item exists")
    fake_db[item.name] = item
    return item
```

**tests/test_main.py:**
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app, fake_db

@pytest.fixture
def client():
    fake_db.clear()  # Clean database before each test
    return TestClient(app)

@pytest.fixture
def auth_headers():
    return {"X-Token": "secret-token"}

def test_read_item(client, auth_headers):
    # Create item first
    client.post(
        "/items/",
        headers=auth_headers,
        json={"name": "foo", "price": 10.5}
    )

    # Read item
    response = client.get("/items/foo", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"name": "foo", "price": 10.5}

def test_read_item_bad_token(client):
    response = client.get("/items/foo", headers={"X-Token": "wrong"})
    assert response.status_code == 400

def test_read_nonexistent_item(client, auth_headers):
    response = client.get("/items/nonexistent", headers=auth_headers)
    assert response.status_code == 404

def test_create_item(client, auth_headers):
    response = client.post(
        "/items/",
        headers=auth_headers,
        json={"name": "test", "price": 99.9}
    )
    assert response.status_code == 201
    assert response.json() == {"name": "test", "price": 99.9}

def test_create_duplicate_item(client, auth_headers):
    item_data = {"name": "duplicate", "price": 10.0}

    # Create first time
    client.post("/items/", headers=auth_headers, json=item_data)

    # Try to create again
    response = client.post("/items/", headers=auth_headers, json=item_data)
    assert response.status_code == 409
```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_main.py

# Run specific test
pytest tests/test_main.py::test_read_main

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app tests/
```

## Key Points

- Use `TestClient` from `fastapi.testclient`
- Write regular `def` functions, not `async def`
- Don't use `await` with TestClient
- Override dependencies for testing
- Use pytest fixtures for setup/teardown
- Test success cases and error cases
- Use parametrized tests for multiple scenarios
- Clean test data between tests
- TestClient handles application lifecycle automatically
