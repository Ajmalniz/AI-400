# Testing Quick Reference - Task Management API

## 🚀 Quick Start

### Run All Tests
```bash
uv run pytest -v
```
**Expected:** 41 passed in ~0.7s

---

## 📋 Common Test Commands

### Basic Commands

```bash
# Run all tests with verbose output
uv run pytest -v

# Run tests without verbose output
uv run pytest

# Run with even more detail
uv run pytest -vv

# Show print statements
uv run pytest -v -s
```

### Test Selection

```bash
# Run smoke tests only (3 critical tests)
uv run pytest -v -k "smoke"

# Run integration tests only
uv run pytest -v -m integration

# Run specific test file
uv run pytest -v tests/test_main.py

# Run specific test class
uv run pytest -v tests/test_main.py::TestTasksEndpoint

# Run specific test
uv run pytest -v tests/test_main.py::TestRootEndpoint::test_root_returns_welcome_message

# Run tests matching pattern
uv run pytest -k "error" -v          # All error tests
uv run pytest -k "search" -v         # All search tests
uv run pytest -k "task" -v           # All task-related tests
uv run pytest -k "not integration" -v # Exclude integration tests
```

### Coverage Reports

```bash
# Run with coverage (terminal output)
uv run pytest --cov=. --cov-report=term

# Run with coverage showing missing lines
uv run pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
uv run pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# Generate XML coverage report (for CI/CD)
uv run pytest --cov=. --cov-report=xml

# All coverage formats
uv run pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=xml
```

### Debugging

```bash
# Stop at first failure
uv run pytest -x

# Stop after N failures
uv run pytest --maxfail=3

# Show local variables on failure
uv run pytest -l

# Full traceback
uv run pytest --tb=long

# Short traceback (default)
uv run pytest --tb=short

# No traceback
uv run pytest --tb=no

# Enter debugger on failure
uv run pytest --pdb
```

### Output Control

```bash
# Quiet mode (less output)
uv run pytest -q

# Very quiet (only test results)
uv run pytest -qq

# Show summary of all test outcomes
uv run pytest -ra

# Show summary of failures only
uv run pytest -rf

# Show captured output for failed tests
uv run pytest --capture=no

# Disable output capturing
uv run pytest -s
```

---

## 📊 Test Organization

### By Category

```bash
# Root endpoint tests (3 tests)
uv run pytest -v tests/test_main.py::TestRootEndpoint

# Tasks endpoint success tests (8 tests)
uv run pytest -v tests/test_main.py::TestTasksEndpoint

# Tasks endpoint error tests (9 tests)
uv run pytest -v tests/test_main.py::TestTasksEndpointErrors

# Search endpoint tests (10 tests)
uv run pytest -v tests/test_main.py::TestSearchEndpoint

# Search endpoint error tests (6 tests)
uv run pytest -v tests/test_main.py::TestSearchEndpointErrors

# Pagination tests (2 tests)
uv run pytest -v tests/test_main.py::TestPaginationConsistency

# API contract tests (3 tests)
uv run pytest -v tests/test_main.py::TestAPIContractStability

# Integration tests (2 tests)
uv run pytest -v tests/test_main.py::TestAPIIntegration
```

---

## 🎯 Useful Combinations

### Quick Smoke Check (Fast)
```bash
uv run pytest -v -k "smoke"
# Runs 3 critical tests in ~0.08s
```

### Pre-Commit Check
```bash
uv run pytest -v --cov=. --cov-report=term-missing
# Ensures all tests pass with coverage info
```

### Debugging Failed Test
```bash
uv run pytest -v -x -l --pdb tests/test_main.py::TestTasksEndpoint::test_get_task_by_id_success
# -x: Stop at first failure
# -l: Show local variables
# --pdb: Enter debugger
```

### CI/CD Pipeline
```bash
uv run pytest -v --cov=. --cov-report=xml --cov-report=html --junitxml=junit.xml
# Generates reports for CI systems
```

### Watch Mode (with pytest-watch)
```bash
# First: uv add --dev pytest-watch
uv run ptw -- -v
# Auto-runs tests on file changes
```

---

## 🔍 Test Markers

### Available Markers

```ini
# Defined in pytest.ini
smoke: Quick smoke tests for critical functionality
integration: Integration tests
unit: Unit tests
```

### Using Markers

```bash
# Run smoke tests
uv run pytest -v -m smoke

# Run integration tests
uv run pytest -v -m integration

# Run unit tests
uv run pytest -v -m unit

# Run all except integration
uv run pytest -v -m "not integration"

# Combine markers
uv run pytest -v -m "smoke or integration"
```

---

## 📈 Performance Profiling

### Duration Report

```bash
# Show slowest 10 tests
uv run pytest --durations=10

# Show all test durations
uv run pytest --durations=0

# Show slowest tests with verbose output
uv run pytest -v --durations=5
```

### Parallel Execution (with pytest-xdist)

```bash
# First: uv add --dev pytest-xdist
uv run pytest -n auto  # Use all CPU cores
uv run pytest -n 4     # Use 4 processes
```

---

## 🛠️ Configuration Files

### pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short --strict-markers --color=yes
markers =
    smoke: Quick smoke tests
    integration: Integration tests
    unit: Unit tests
```

### pyproject.toml (pytest section)
```toml
[tool.pytest.ini_options]
# Alternative to pytest.ini
testpaths = ["tests"]
python_files = ["test_*.py"]
```

---

## 🐛 Common Issues

### Issue: Tests not found
```bash
# Check test discovery
uv run pytest --collect-only

# Verify pytest can find tests
uv run pytest -v --collect-only tests/
```

### Issue: Import errors
```bash
# Ensure using uv run
uv run pytest -v  # ✅ Correct

# NOT: pytest -v  # ❌ Uses system Python
```

### Issue: Coverage not working
```bash
# Reinstall pytest-cov
uv add --dev pytest-cov --reload

# Verify installation
uv run pytest --version
```

---

## 📝 Writing New Tests

### Test Template

```python
class TestNewFeature:
    """Tests for new feature."""

    def test_feature_success(self, client):
        """Test feature works correctly."""
        response = client.get("/new-endpoint")

        assert response.status_code == 200
        data = response.json()
        assert "expected_field" in data

    def test_feature_error(self, client):
        """Test feature handles errors correctly."""
        response = client.get("/new-endpoint?invalid=param")

        assert response.status_code == 422
        assert "detail" in response.json()
```

### Run New Test

```bash
# Run just your new test class
uv run pytest -v tests/test_main.py::TestNewFeature

# Run in watch mode while developing
uv run ptw tests/test_main.py::TestNewFeature -- -v
```

---

## 🎯 Test Coverage Goals

### Current Coverage
- **main.py:** 100% ✅
- **Overall:** 98% ✅

### Checking Coverage

```bash
# Quick coverage check
uv run pytest --cov=main --cov-report=term

# Detailed with missing lines
uv run pytest --cov=main --cov-report=term-missing

# HTML report for browsing
uv run pytest --cov=. --cov-report=html
# Open htmlcov/index.html
```

---

## 🚀 Production Readiness Checklist

Before deploying:

```bash
# 1. Run all tests
uv run pytest -v
# Expected: 41 passed

# 2. Check coverage
uv run pytest --cov=. --cov-report=term-missing
# Expected: 98%+ coverage

# 3. Run smoke tests
uv run pytest -v -k "smoke"
# Expected: 3 passed in ~0.08s

# 4. Run integration tests
uv run pytest -v -m integration
# Expected: 2 passed

# 5. Generate coverage report
uv run pytest --cov=. --cov-report=html
# Review htmlcov/index.html

# All green? Ready to deploy! ✅
```

---

## 📚 Additional Resources

### Documentation
- FastAPI Skill: `.claude/skills/fastapi/SKILL.md`
- Testing Reference: `.claude/skills/fastapi/references/testing.md`
- Test Suite Summary: `TEST_SUITE_SUMMARY.md`

### Commands Help
```bash
# Pytest help
uv run pytest --help

# Show available fixtures
uv run pytest --fixtures

# Show available markers
uv run pytest --markers
```

---

## 💡 Pro Tips

1. **Always use `uv run`** - Ensures correct virtual environment
   ```bash
   uv run pytest -v  # ✅ Correct
   pytest -v         # ❌ Wrong - uses system Python
   ```

2. **Run smoke tests frequently** - Fast feedback loop
   ```bash
   uv run pytest -k "smoke"  # ~0.08s
   ```

3. **Use `-x` during debugging** - Stop at first failure
   ```bash
   uv run pytest -x -v
   ```

4. **Check coverage regularly** - Maintain high coverage
   ```bash
   uv run pytest --cov=. --cov-report=term-missing
   ```

5. **Use markers** - Organize tests by type
   ```bash
   uv run pytest -m smoke      # Quick checks
   uv run pytest -m integration # Full workflows
   ```

---

## 🎉 Quick Win Commands

```bash
# 1. Verify everything works
uv run pytest -v

# 2. Quick smoke check
uv run pytest -k "smoke" -v

# 3. Coverage report
uv run pytest --cov=. --cov-report=term-missing

# 4. Debug a failing test
uv run pytest -v -x -l --pdb -k "test_name"

# 5. Generate HTML coverage
uv run pytest --cov=. --cov-report=html
```

**That's it! Happy testing! 🚀**
