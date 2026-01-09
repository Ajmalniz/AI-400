from fastapi import FastAPI

app = FastAPI(
    title="Task Management API",
    description="A simple API demonstrating FastAPI best practices",
    version="1.0.0"
)


@app.get("/")
async def get_welcome_message():
    """Root endpoint that returns a welcome message"""
    return {
        "message": "Welcome to the Task Management API!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    """
    Get a task by ID using path parameter

    Args:
        task_id: The unique identifier for the task (must be an integer)

    Returns:
        Dictionary containing task details
    """
    return {
        "task_id": task_id,
        "title": f"Task #{task_id}",
        "description": f"This is task number {task_id}",
        "status": "pending",
        "priority": "medium",
        "created_at": "2026-01-09T00:00:00Z"
    }


@app.get("/search")
async def search_tasks(
    q: str,
    limit: int = 10,
    offset: int = 0,
    status: str | None = None
):
    """
    Search tasks with query parameters

    Args:
        q: Search query string (required)
        limit: Maximum number of results to return (default: 10)
        offset: Number of results to skip for pagination (default: 0)
        status: Optional filter by task status

    Returns:
        Dictionary containing search results and metadata
    """
    return {
        "query": q,
        "filters": {
            "status": status,
            "limit": limit,
            "offset": offset
        },
        "total_results": 42,
        "results": [
            {
                "task_id": offset + 1,
                "title": f"Task matching '{q}'",
                "status": status or "pending",
                "relevance_score": 0.95
            },
            {
                "task_id": offset + 2,
                "title": f"Another task for '{q}'",
                "status": status or "in_progress",
                "relevance_score": 0.87
            }
        ]
    }
