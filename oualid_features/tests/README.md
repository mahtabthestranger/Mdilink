# Unit Tests for Al Mamun Oualid's Features

## F3: Doctor Login - Unit Tests

### Running the Tests

Option 1: Run with Python
```bash
cd f:\medilink4
python -m unittest oualid_features.tests.test_doctor_login
```

Option 2: Run with pytest (if installed)
```bash
cd f:\medilink4
pytest oualid_features/tests/test_doctor_login.py -v
```

Option 3: Run directly
```bash
cd f:\medilink4
python oualid_features/tests/test_doctor_login.py
```

### Test Cases Covered

1. test_verify_password_valid_credentials
- Purpose: Tests successful doctor login with correct credentials
- Expected: Returns doctor information
- Covers: F3 Confirmation Criteria

2. test_verify_password_invalid_credentials
- Purpose: Tests login failure with wrong password
- Expected: Returns None
- Covers: F3 Confirmation Criteria

3. test_verify_password_nonexistent_doctor
- Purpose: Tests login with non-existent doctor code
- Expected: Returns None
- Covers: Input validation

4. test_find_by_code_active_doctor
- Purpose: Tests finding doctor by code
- Expected: Returns active doctor information
- Covers: Database query functionality

5. test_password_hashing
- Purpose: Tests password is hashed before storing
- Expected: Password is hashed using generate_password_hash
- Covers: Security requirement from coding standard

### Expected Output

When you run the tests, you should see:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK
```

### Test Results

All 5 tests should PASS

This demonstrates:
- Valid login works correctly
- Invalid credentials are rejected
- Non-existent doctors cannot login
- Password hashing is implemented
- Database queries work properly

---

Author: Al Mamun Oualid
Feature: F3 - Doctor Login
Date: December 2025
