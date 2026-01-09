# Dependency Injection Reference

Complete guide to FastAPI's dependency injection system for code reuse, database connections, authentication, and more.

## Table of Contents
- What is Dependency Injection
- Basic Dependencies
- Sharing Dependencies with Annotated
- Classes as Dependencies
- Sub-dependencies
- Dependencies in Path Operation Decorators
- Global Dependencies
- Dependencies with Yield

## What is Dependency Injection

Dependency Injection means path operation functions can declare requirements, and FastAPI automatically provides them.

**Use cases:**
- Shared logic and code reuse
- Database connections
- Security and authentication
- Permission/role requirements
- Data validation
- Minimizing code repetition

## Basic Dependencies

### Creating a Dependency

A dependency is a function that accepts the same parameter types as path operations:

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}
```

### Using Dependencies

Use `Depends()` to declare dependencies:

```python
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

**Important:** Pass the function to `Depends()` without calling it (no parentheses).

## Sharing Dependencies with Annotated

Reduce duplication by storing dependencies as type aliases:

```python
from typing import Annotated
from fastapi import Depends

CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons

@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons
```

**Benefits:**
- Single source of truth
- Preserves type information
- Editor autocompletion works
- Compatible with type checkers like mypy

## Classes as Dependencies

Classes can be used as dependencies for stateful logic:

```python
from typing import Annotated
from fastapi import Depends

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    response.update({"skip": commons.skip, "limit": commons.limit})
    return response
```

**Shortcut when class and type are the same:**

```python
@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    return commons
```

## Sub-dependencies

Dependencies can have their own dependencies, creating a tree:

```python
from fastapi import Cookie

def query_extractor(q: str | None = None):
    return q

def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str | None, Cookie()] = None
):
    if not q:
        return last_query
    return q

@app.get("/items/")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
):
    return {"q_or_cookie": query_or_default}
```

**How it works:**
1. FastAPI calls `query_extractor`
2. Result passed to `query_or_cookie_extractor`
3. Final result passed to `read_query`

## Common Dependency Patterns

### Database Session

```python
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
async def read_users(db: Annotated[Session, Depends(get_db)]):
    users = db.query(User).all()
    return users
```

### Current User

```python
from fastapi import HTTPException, Header

async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token

async def get_current_user(token: Annotated[str, Depends(get_token_header)]):
    # Validate token and get user
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
```

### Pagination

```python
def pagination_params(skip: int = 0, limit: int = 100):
    return {"skip": skip, "limit": limit}

PaginationDep = Annotated[dict, Depends(pagination_params)]

@app.get("/items/")
async def read_items(pagination: PaginationDep):
    return fake_items_db[pagination["skip"]:pagination["skip"] + pagination["limit"]]
```

## Dependencies in Path Operation Decorators

For dependencies that don't return values (side effects only):

```python
from fastapi import Depends, HTTPException

async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
```

**Use case:** Authentication/validation without using the result.

## Global Dependencies

Apply dependencies to all path operations:

```python
app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
```

Or to a router:

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(verify_token)]
)

@router.get("/")
async def read_items():
    return [{"item": "Foo"}]
```

## Dependencies with Yield

Use `yield` for setup/teardown logic (e.g., database connections):

```python
async def get_db():
    db = SessionLocal()
    try:
        yield db  # This is injected into path operation
    finally:
        db.close()  # Cleanup after response is sent

@app.get("/users/")
async def read_users(db: Annotated[Session, Depends(get_db)]):
    users = db.query(User).all()
    return users
```

**Execution flow:**
1. Code before `yield` runs before request processing
2. Yielded value is injected
3. Path operation executes
4. Code after `yield` runs after response is sent

### Yield with Try/Except

```python
async def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

### Sub-dependencies with Yield

```python
async def dependency_a():
    print("dependency_a: start")
    dep_a = {"value": "from dependency_a"}
    yield dep_a
    print("dependency_a: cleanup")

async def dependency_b(dep_a: Annotated[dict, Depends(dependency_a)]):
    print("dependency_b: start")
    dep_b = {"value": "from dependency_b", "parent": dep_a}
    yield dep_b
    print("dependency_b: cleanup")

@app.get("/")
async def read_main(dep_b: Annotated[dict, Depends(dependency_b)]):
    return dep_b
```

**Execution order:**
1. `dependency_a` start
2. `dependency_b` start
3. Path operation
4. `dependency_b` cleanup
5. `dependency_a` cleanup

## Async Considerations

You can mix `async def` and `def` dependencies freely:

```python
async def async_dependency():
    # Can use await
    return {"key": "value"}

def sync_dependency():
    # Regular function
    return {"key": "value"}

@app.get("/async-path/")
async def async_path(
    dep1: Annotated[dict, Depends(async_dependency)],
    dep2: Annotated[dict, Depends(sync_dependency)]
):
    return {"dep1": dep1, "dep2": dep2}

@app.get("/sync-path/")
def sync_path(
    dep1: Annotated[dict, Depends(async_dependency)],
    dep2: Annotated[dict, Depends(sync_dependency)]
):
    return {"dep1": dep1, "dep2": dep2}
```

FastAPI handles the execution appropriately.

## Key Points

- Dependencies are regular functions with the same parameters as path operations
- Use `Depends()` to declare dependencies
- Store shared dependencies in `Annotated` type aliases
- Dependencies can have sub-dependencies (tree structure)
- Use `yield` for setup/teardown logic
- Dependencies execute automatically for every request
- All validation and documentation benefits apply to dependencies
- Mix `async` and `sync` dependencies freely
