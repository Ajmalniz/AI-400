# Path Operations Reference

Complete guide to handling path operations, parameters, request bodies, and responses in FastAPI.

## Table of Contents
- HTTP Methods and Decorators
- Path Parameters
- Query Parameters
- Request Body
- Response Models
- Multiple Parameters
- Data Validation

## HTTP Methods and Decorators

FastAPI provides decorators for all HTTP methods:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")        # Read
async def read_items():
    pass

@app.post("/items/")       # Create
async def create_item():
    pass

@app.put("/items/{id}")    # Update (full)
async def update_item(id: int):
    pass

@app.patch("/items/{id}")  # Update (partial)
async def patch_item(id: int):
    pass

@app.delete("/items/{id}") # Delete
async def delete_item(id: int):
    pass
```

## Path Parameters

### Basic Path Parameters with Type Hints

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

**Benefits:**
- Automatic parsing (string → int)
- Data validation
- Editor support
- Auto-documentation

### Predefined Values with Enums

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

### Path Parameters with File Paths

Use `:path` converter for paths containing slashes:

```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

**Example:** `/files/home/user/file.txt` → `{"file_path": "home/user/file.txt"}`

### Route Order Matters

Fixed paths must be declared **before** parameterized paths:

```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")  # Declare AFTER fixed paths
async def read_user(user_id: str):
    return {"user_id": user_id}
```

## Query Parameters

Query parameters are function parameters not in the path.

### Basic Query Parameters

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

**URL:** `http://localhost:8000/items/?skip=20&limit=10`

### Optional Query Parameters

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

### Boolean Query Parameters

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, short: bool = False):
    item = {"item_id": item_id}
    if not short:
        item.update({"description": "Long description here"})
    return item
```

**Bool conversion:** `?short=1`, `?short=True`, `?short=yes`, `?short=on` → `True`

### Required Query Parameters

Omit default value to make required:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, needy: str):  # needy is required
    return {"item_id": item_id, "needy": needy}
```

### Multiple Parameter Types

```python
@app.get("/items/{item_id}")
async def read_item(
    item_id: str,              # required path parameter
    needy: str,                # required query parameter
    skip: int = 0,             # optional with default
    limit: int | None = None   # optional, no default
):
    return {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
```

## Request Body

Use Pydantic models for request bodies.

### Basic Request Body

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

**Request:**
```json
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
```

### Using Model Data

```python
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
```

### Request Body + Path Parameters

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}
```

### Request Body + Path + Query Parameters

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
```

**Parameter Recognition:**
- **Path**: Declared in route (e.g., `{item_id}`)
- **Query**: Singular types with defaults (e.g., `str | None = None`)
- **Body**: Pydantic model parameters

## Response Models

### Basic Response Model

```python
from pydantic import BaseModel

class ItemOut(BaseModel):
    name: str
    price: float

@app.post("/items/", response_model=ItemOut)
async def create_item(item: Item):
    return item  # Only name and price returned
```

### Multiple Response Models

```python
from typing import Union

class UserIn(BaseModel):
    username: str
    password: str
    email: str

class UserOut(BaseModel):
    username: str
    email: str

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    return user  # Password automatically excluded
```

### Response Status Codes

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None
```

## Data Validation

FastAPI/Pydantic provides automatic validation:

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, max_length=300)
    price: float = Field(..., gt=0)  # Greater than 0
    tax: float | None = Field(None, ge=0)  # Greater or equal to 0

@app.post("/items/")
async def create_item(item: Item):
    return item
```

**Validation features:**
- String length: `min_length`, `max_length`
- Numeric: `gt`, `ge`, `lt`, `le`
- Regex patterns: `pattern`
- Custom validators

## Advanced Request Body

### Nested Models

```python
from pydantic import BaseModel

class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    images: list[Image] | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### List Bodies

```python
@app.post("/images/")
async def create_images(images: list[Image]):
    return images
```

### Arbitrary dict Bodies

```python
@app.post("/index-weights/")
async def create_weights(weights: dict[int, float]):
    return weights
```

## Key Points

- Use type hints for automatic validation and documentation
- Order matters: declare fixed paths before parameterized ones
- Pydantic models enable request/response validation
- FastAPI automatically distinguishes path, query, and body parameters
- All validations appear in OpenAPI docs automatically
