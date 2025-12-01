# Medilink Tests

This directory contains unit tests for the Medilink Hospital Management System.

## Running Tests

### Run all tests:
```bash
python -m unittest discover tests
```

### Run specific test file:
```bash
python -m unittest tests.test_auth
python -m unittest tests.test_appointments
python -m unittest tests.test_password_reset
```

### Run with verbose output:
```bash
python -m unittest discover tests -v
```

### Using pytest (if installed):
```bash
pip install pytest
pytest tests/ -v
```

## Test Files

- `test_base.py` - Base test case with database setup
- `test_auth.py` - Authentication tests (login, register, logout)
- `test_appointments.py` - Appointment management tests
- `test_password_reset.py` - Password reset functionality tests

## Test Database

Tests use a separate database (`medilink_test_db`) to avoid affecting your development data.

## Adding New Tests

1. Create a new test file in the `tests/` directory
2. Import `BaseTestCase` from `test_base`
3. Create test class inheriting from `BaseTestCase`
4. Write test methods starting with `test_`

Example:
```python
from tests.test_base import BaseTestCase

class TestMyFeature(BaseTestCase):
    def test_something(self):
        # Your test code
        self.assertEqual(1, 1)
```
