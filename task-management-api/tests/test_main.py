"""
Comprehensive test suite for Task Management API.

Tests follow TDD principles and cover:
- Success cases (happy path)
- Error cases (404, 422 validation)
- Type validation
- Query parameter defaults
- Required vs optional parameters
- Agent-specific contract stability
"""

import pytest
from fastapi.testclient import TestClient


# ============================================================================
# ROOT ENDPOINT TESTS
# ============================================================================

class TestRootEndpoint:
    """Tests for GET / endpoint."""

    @pytest.mark.smoke
    def test_root_returns_welcome_message(self, client):
        """GET / should return welcome message with correct structure."""
        response = client.get("/")

        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "Welcome to the Task Management API!"
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
        assert data["status"] == "operational"

    def test_root_returns_json(self, client):
        """GET / should return JSON content type."""
        response = client.get("/")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

    def test_root_response_schema_stability(self, client):
        """
        GET / response schema should be stable (important for agents).

        Agents depend on consistent field names and types.
        """
        response = client.get("/")
        data = response.json()

        # Verify all expected fields exist
        required_fields = ["message", "version", "docs", "status"]
        for field in required_fields:
            assert field in data, f"Required field '{field}' missing from response"

        # Verify field types (agents can't handle type changes)
        assert isinstance(data["message"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["docs"], str)
        assert isinstance(data["status"], str)


# ============================================================================
# TASKS ENDPOINT TESTS
# ============================================================================

class TestTasksEndpoint:
    """Tests for GET /tasks/{task_id} endpoint."""

    @pytest.mark.smoke
    def test_get_task_by_id_success(self, client, sample_task_id):
        """GET /tasks/{task_id} should return task details."""
        response = client.get(f"/tasks/{sample_task_id}")

        assert response.status_code == 200

        data = response.json()
        assert data["task_id"] == sample_task_id
        assert data["title"] == f"Task #{sample_task_id}"
        assert data["description"] == f"This is task number {sample_task_id}"
        assert data["status"] == "pending"
        assert data["priority"] == "medium"
        assert "created_at" in data

    def test_get_task_with_different_ids(self, client):
        """GET /tasks/{task_id} should work with different task IDs."""
        test_ids = [1, 42, 100, 999, 12345]

        for task_id in test_ids:
            response = client.get(f"/tasks/{task_id}")

            assert response.status_code == 200
            data = response.json()
            assert data["task_id"] == task_id
            assert str(task_id) in data["title"]

    def test_get_task_response_schema_stability(self, client):
        """
        GET /tasks/{task_id} response schema should be stable.

        Critical for agents that depend on consistent field structure.
        """
        response = client.get("/tasks/1")
        data = response.json()

        # Verify all expected fields exist
        required_fields = [
            "task_id",
            "title",
            "description",
            "status",
            "priority",
            "created_at"
        ]
        for field in required_fields:
            assert field in data, f"Required field '{field}' missing"

        # Verify field types
        assert isinstance(data["task_id"], int)
        assert isinstance(data["title"], str)
        assert isinstance(data["description"], str)
        assert isinstance(data["status"], str)
        assert isinstance(data["priority"], str)
        assert isinstance(data["created_at"], str)

    def test_get_task_with_zero_id(self, client):
        """GET /tasks/0 should return task with ID 0."""
        response = client.get("/tasks/0")

        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == 0

    def test_get_task_with_negative_id(self, client):
        """GET /tasks/{negative_id} should work (no validation preventing it)."""
        response = client.get("/tasks/-1")

        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == -1


# ============================================================================
# TASKS ENDPOINT - ERROR CASES
# ============================================================================

class TestTasksEndpointErrors:
    """Tests for error cases in GET /tasks/{task_id}."""

    def test_get_task_with_invalid_id_type_string(self, client):
        """GET /tasks/{task_id} should reject non-integer IDs with 422."""
        response = client.get("/tasks/invalid-id")

        assert response.status_code == 422

        data = response.json()
        assert "detail" in data

        # Verify error details
        error = data["detail"][0]
        assert error["type"] == "int_parsing"
        assert "task_id" in str(error["loc"])

    def test_get_task_with_invalid_id_type_float(self, client):
        """GET /tasks/{task_id} should reject float IDs with 422."""
        response = client.get("/tasks/123.45")

        assert response.status_code == 422
        assert "detail" in response.json()

    def test_get_task_with_invalid_id_type_uuid(self, client):
        """GET /tasks/{task_id} should reject UUID format with 422."""
        response = client.get("/tasks/550e8400-e29b-41d4-a716-446655440000")

        assert response.status_code == 422
        assert "detail" in response.json()

    @pytest.mark.parametrize("invalid_id", [
        "abc",
        "task_123",
        "null",
        "undefined",
        " ",
        "12.34.56",
    ])
    def test_get_task_with_various_invalid_ids(self, client, invalid_id):
        """
        GET /tasks/{task_id} should reject various invalid ID formats.

        Using parametrize to test multiple invalid inputs efficiently.
        """
        response = client.get(f"/tasks/{invalid_id}")

        assert response.status_code == 422
        assert "detail" in response.json()

    def test_get_task_with_empty_string_id(self, client):
        """
        GET /tasks/ (empty ID) should return 404.

        Empty string creates /tasks/ which doesn't match /tasks/{task_id} pattern.
        """
        response = client.get("/tasks/")

        # Empty path segment results in different route, returns 404
        assert response.status_code == 404


# ============================================================================
# SEARCH ENDPOINT TESTS
# ============================================================================

class TestSearchEndpoint:
    """Tests for GET /search endpoint."""

    @pytest.mark.smoke
    def test_search_with_required_query_param(self, client):
        """GET /search?q=... should return search results."""
        response = client.get("/search?q=test")

        assert response.status_code == 200

        data = response.json()
        assert data["query"] == "test"
        assert "filters" in data
        assert "total_results" in data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_search_with_all_parameters(self, client):
        """GET /search with all parameters should apply filters correctly."""
        response = client.get(
            "/search?q=fastapi&limit=5&offset=10&status=completed"
        )

        assert response.status_code == 200

        data = response.json()
        assert data["query"] == "fastapi"
        assert data["filters"]["limit"] == 5
        assert data["filters"]["offset"] == 10
        assert data["filters"]["status"] == "completed"

    def test_search_with_default_limit_and_offset(self, client):
        """GET /search should use default values for limit and offset."""
        response = client.get("/search?q=test")

        assert response.status_code == 200

        data = response.json()
        assert data["filters"]["limit"] == 10  # Default limit
        assert data["filters"]["offset"] == 0  # Default offset
        assert data["filters"]["status"] is None  # Optional, not provided

    def test_search_with_custom_limit(self, client):
        """GET /search should accept custom limit values."""
        for limit in [1, 5, 20, 100]:
            response = client.get(f"/search?q=test&limit={limit}")

            assert response.status_code == 200
            data = response.json()
            assert data["filters"]["limit"] == limit

    def test_search_with_custom_offset(self, client):
        """GET /search should accept custom offset values for pagination."""
        for offset in [0, 10, 50, 100]:
            response = client.get(f"/search?q=test&offset={offset}")

            assert response.status_code == 200
            data = response.json()
            assert data["filters"]["offset"] == offset

    def test_search_with_status_filter(self, client):
        """GET /search should accept optional status filter."""
        statuses = ["pending", "in_progress", "completed", "cancelled"]

        for status in statuses:
            response = client.get(f"/search?q=test&status={status}")

            assert response.status_code == 200
            data = response.json()
            assert data["filters"]["status"] == status

    def test_search_without_status_filter(self, client):
        """GET /search without status should have null status filter."""
        response = client.get("/search?q=test")

        assert response.status_code == 200
        data = response.json()
        assert data["filters"]["status"] is None

    def test_search_results_structure(self, client):
        """GET /search results should have correct structure."""
        response = client.get("/search?q=test")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data["results"], list)
        assert len(data["results"]) > 0

        # Check first result structure
        result = data["results"][0]
        assert "task_id" in result
        assert "title" in result
        assert "status" in result
        assert "relevance_score" in result

    def test_search_query_reflected_in_results(self, client):
        """GET /search should reflect query string in results."""
        query = "my special query"
        response = client.get(f"/search?q={query}")

        assert response.status_code == 200
        data = response.json()

        assert data["query"] == query
        # Results should contain the query string
        for result in data["results"]:
            assert query in result["title"]

    def test_search_response_schema_stability(self, client):
        """
        GET /search response schema should be stable for agents.

        Agents depend on consistent top-level fields.
        """
        response = client.get("/search?q=test")
        data = response.json()

        # Verify all expected top-level fields
        required_fields = ["query", "filters", "total_results", "results"]
        for field in required_fields:
            assert field in data, f"Required field '{field}' missing"

        # Verify filters structure
        assert "status" in data["filters"]
        assert "limit" in data["filters"]
        assert "offset" in data["filters"]

        # Verify types
        assert isinstance(data["query"], str)
        assert isinstance(data["filters"], dict)
        assert isinstance(data["total_results"], int)
        assert isinstance(data["results"], list)


# ============================================================================
# SEARCH ENDPOINT - ERROR CASES
# ============================================================================

class TestSearchEndpointErrors:
    """Tests for error cases in GET /search."""

    def test_search_without_query_param(self, client):
        """GET /search without required 'q' param should return 422."""
        response = client.get("/search")

        assert response.status_code == 422

        data = response.json()
        assert "detail" in data

        # Verify error indicates missing 'q' parameter
        error = data["detail"][0]
        assert error["type"] == "missing"
        assert "q" in str(error["loc"])

    def test_search_with_empty_query(self, client):
        """GET /search with empty query string should work (empty string is valid)."""
        response = client.get("/search?q=")

        # Empty string is a valid string, should return 200
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == ""

    def test_search_with_invalid_limit_type(self, client):
        """GET /search with non-integer limit should return 422."""
        response = client.get("/search?q=test&limit=invalid")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_search_with_invalid_offset_type(self, client):
        """GET /search with non-integer offset should return 422."""
        response = client.get("/search?q=test&offset=abc")

        assert response.status_code == 422
        assert "detail" in response.json()

    def test_search_with_negative_limit(self, client):
        """GET /search with negative limit should work (no validation preventing it)."""
        response = client.get("/search?q=test&limit=-1")

        # No validation preventing negative values in current implementation
        assert response.status_code == 200

    def test_search_with_negative_offset(self, client):
        """GET /search with negative offset should work (no validation preventing it)."""
        response = client.get("/search?q=test&offset=-10")

        # No validation preventing negative values in current implementation
        assert response.status_code == 200


# ============================================================================
# PAGINATION CONSISTENCY TESTS (Agent-Specific)
# ============================================================================

class TestPaginationConsistency:
    """
    Tests for pagination consistency.

    Important for agents that iterate through paginated results.
    """

    def test_pagination_offset_affects_results(self, client):
        """Different offsets should return different task IDs."""
        response1 = client.get("/search?q=test&offset=0")
        response2 = client.get("/search?q=test&offset=10")

        assert response1.status_code == 200
        assert response2.status_code == 200

        data1 = response1.json()
        data2 = response2.json()

        # Task IDs should be different
        ids1 = {result["task_id"] for result in data1["results"]}
        ids2 = {result["task_id"] for result in data2["results"]}

        assert ids1 != ids2  # Different pages should have different IDs

    def test_pagination_limit_affects_result_count(self, client):
        """
        Limit parameter should affect number of results.

        Note: In current mock implementation, always returns 2 results.
        This test documents expected behavior for future implementation.
        """
        response = client.get("/search?q=test&limit=5")

        assert response.status_code == 200
        data = response.json()

        # Current implementation always returns 2 results (mock data)
        # In real implementation, should respect limit
        assert len(data["results"]) <= data["filters"]["limit"]


# ============================================================================
# API CONTRACT STABILITY TESTS (Agent-Specific)
# ============================================================================

class TestAPIContractStability:
    """
    Tests to ensure API contract remains stable for agent consumers.

    These tests verify that response formats don't change unexpectedly,
    which would break agents that depend on the API.
    """

    def test_all_endpoints_return_json(self, client):
        """All endpoints should return JSON content type."""
        endpoints = [
            "/",
            "/tasks/1",
            "/search?q=test"
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            assert "application/json" in response.headers["content-type"]

    def test_all_endpoints_return_dictionaries(self, client):
        """
        All endpoints should return dictionaries (never None or primitives).

        This is a critical principle from the fastapi skill.
        """
        endpoints = [
            "/",
            "/tasks/1",
            "/search?q=test"
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, dict), f"Endpoint {endpoint} didn't return dict"
            assert data is not None, f"Endpoint {endpoint} returned None"

    def test_error_responses_have_consistent_format(self, client):
        """
        Error responses should have consistent 'detail' field.

        Agents need predictable error formats.
        """
        # Test 422 validation error
        response = client.get("/tasks/invalid")
        assert response.status_code == 422
        assert "detail" in response.json()

        # Test missing required parameter
        response = client.get("/search")
        assert response.status_code == 422
        assert "detail" in response.json()


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests for complete workflows."""

    def test_complete_search_workflow(self, client):
        """Test complete search workflow: query -> paginate -> filter."""
        # Step 1: Search with query
        response1 = client.get("/search?q=project")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["query"] == "project"

        # Step 2: Paginate to next page
        response2 = client.get("/search?q=project&offset=10")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["filters"]["offset"] == 10

        # Step 3: Filter by status
        response3 = client.get("/search?q=project&status=completed")
        assert response3.status_code == 200
        data3 = response3.json()
        assert data3["filters"]["status"] == "completed"

    def test_api_discovery_workflow(self, client):
        """Test API discovery: root -> docs -> specific endpoints."""
        # Step 1: Get root information
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["docs"] == "/docs"

        # Step 2: Access tasks endpoint
        response = client.get("/tasks/1")
        assert response.status_code == 200

        # Step 3: Use search endpoint
        response = client.get("/search?q=test")
        assert response.status_code == 200
