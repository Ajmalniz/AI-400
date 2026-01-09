"""
Pytest configuration and shared fixtures.

This file is automatically loaded by pytest and provides
shared fixtures available to all test files.
"""

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance.

    The TestClient handles the application lifecycle automatically,
    so you don't need to start/stop the server manually.

    Usage:
        def test_something(client):
            response = client.get("/endpoint")
            assert response.status_code == 200
    """
    return TestClient(app)


@pytest.fixture
def sample_task_id():
    """Fixture that provides a sample task ID for testing."""
    return 123


@pytest.fixture
def sample_search_query():
    """Fixture that provides a sample search query."""
    return "test query"
