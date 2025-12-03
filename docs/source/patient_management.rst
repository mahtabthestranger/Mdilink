================================================================================
Patient Management - CRUD Operations
================================================================================

Patient Management Overview
=============================

The patient management module provides complete operations for managing patients
in the Medilink system, including CRUD operations and patient record viewing.

Route Summary
=============

.. list-table::
   :widths: 25 15 15 45
   :header-rows: 1

   * - Route
     - Method
     - Auth
     - Description
   * - /admin/patients
     - GET
     - Admin
     - List all active patients
   * - /admin/patients/edit/<id>
     - GET, POST
     - Admin
     - Edit patient information
   * - /admin/patients/delete/<id>
     - POST
     - Admin
     - Delete/deactivate patient

List Patients
=============

**Endpoint**: ``/admin/patients``

**Methods**: GET

**Description**

Displays a paginated list of all active patients with search and filter options.

Request
-------

.. code-block:: bash

    GET /admin/patients
    GET /admin/patients?search=smith&page=1&status=active

**Query Parameters**

.. list-table::
   :widths: 15 15 15 55
   :header-rows: 1

   * - Parameter
     - Type
     - Default
     - Description
   * - search
     - string
     - (empty)
     - Search patients by name, email, phone
   * - page
     - integer
     - 1
     - Page number for pagination
   * - status
     - string
     - active
     - Filter by status (active, inactive)
   * - sort
     - string
     - created_at
     - Sort by field (created_at, name, email)

Response - Success
------------------

**Status Code**: 200 (OK)

**Content-Type**: text/html

**Rendered Template**: admin/patients.html

**Response Data**

.. code-block:: python

    {
        'patients': [
            {
                'patient_id': 1,
                'full_name': 'John Smith',
                'email': 'john.smith@email.com',
                'phone': '555-0100',
                'date_of_birth': '1985-03-15',
                'gender': 'M',
                'address': '123 Main St, City, State',
                'is_active': 1,
                'created_at': '2023-01-20 10:30:00',
                'updated_at': '2024-01-15 14:20:00'
            },
        ],
        'total_count': 240,
        'page': 1,
        'per_page': 10,
        'total_pages': 24
    }

Database Query
--------------

.. code-block:: sql

    SELECT * FROM patients
    WHERE is_active = 1
    AND (full_name LIKE %search% 
         OR email LIKE %search% 
         OR phone LIKE %search%)
    ORDER BY created_at DESC
    LIMIT 10 OFFSET 0

Edit Patient
============

**Endpoint**: ``/admin/patients/edit/<id>``

**Methods**: GET, POST

**Parameters**

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - id
     - integer
     - Patient ID to edit

**Description**

Form to edit patient's personal information (not medical records).

Request (GET)
-------------

.. code-block:: bash

    GET /admin/patients/edit/42

Response (GET)
~~~~~~~~~~~~~~

**Status Code**: 200 (OK)

**Content**: Pre-filled edit form with patient data

**Form Fields**

.. list-table::
   :widths: 20 20 15 45
   :header-rows: 1

   * - Field
     - Type
     - Required
     - Validation
   * - full_name
     - text
     - Yes
     - 2-100 characters, letters/spaces
   * - email
     - email
     - Yes
     - Valid email, unique
   * - phone
     - tel
     - Yes
     - Valid phone format, unique
   * - date_of_birth
     - date
     - No
     - Valid date, patient age 0-150
   * - gender
     - select
     - No
     - M, F, Other, Prefer not to say
   * - address
     - textarea
     - No
     - 0-200 characters
   * - city
     - text
     - No
     - City name
   * - state
     - text
     - No
     - State/Province
   * - postal_code
     - text
     - No
     - Postal code
   * - emergency_contact
     - text
     - No
     - Contact person name
   * - emergency_phone
     - tel
     - No
     - Emergency contact phone

Request (POST)
--------------

.. code-block:: bash

    POST /admin/patients/edit/42
    Content-Type: application/x-www-form-urlencoded

    full_name=John%20Anderson&email=john.a@email.com&phone=555-4321&
    date_of_birth=1985-03-15&gender=M&address=456%20Oak%20Ave&
    city=Springfield&state=IL&postal_code=62701

Response (POST) - Success
--------------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/patients

**Flash Message**: "Patient updated successfully!"

**Database Changes**

.. code-block:: sql

    UPDATE patients
    SET full_name = 'John Anderson',
        email = 'john.a@email.com',
        phone = '555-4321',
        date_of_birth = '1985-03-15',
        gender = 'M',
        address = '456 Oak Ave',
        city = 'Springfield',
        state = 'IL',
        postal_code = '62701',
        updated_at = NOW()
    WHERE patient_id = 42

Response (POST) - Validation Error
-----------------------------------

**Status Code**: 200 (OK)

**Response**: Re-rendered form with error messages

**Possible Errors**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error
     - Cause
   * - "Full name is required"
     - Empty full_name field
   * - "Invalid email format"
     - Malformed email address
   * - "Email already in use"
     - Email assigned to another patient
   * - "Phone already in use"
     - Phone assigned to another patient
   * - "Invalid date of birth"
     - Date format or age validation failed
   * - "Invalid gender selection"
     - Gender not from predefined list
   * - "Address too long"
     - Address exceeds 200 characters

Response (POST) - Server Error
-------------------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/patients/edit/42

**Flash Message**: "Error updating patient"

Delete Patient
==============

**Endpoint**: ``/admin/patients/delete/<id>``

**Methods**: POST

**Description**

Soft-delete (deactivate) a patient. Data preserved in database.

Request
-------

.. code-block:: bash

    POST /admin/patients/delete/42

**Optional Parameters**

.. list-table::
   :widths: 20 15 65
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - confirm
     - string
     - "yes" to confirm deletion
   * - reason
     - string
     - Reason for deletion (optional)

Response - Success
------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/patients

**Flash Message**: "Patient deleted successfully"

**Database Changes**

Soft delete (mark inactive):

.. code-block:: sql

    UPDATE patients
    SET is_active = 0,
        deleted_at = NOW()
    WHERE patient_id = 42

Response - Error
----------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/patients

**Flash Message**: "Patient not found"

**Possible Errors**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error
     - Cause
   * - "Patient not found"
     - Invalid patient ID
   * - "Cannot delete - active appointments"
     - Patient has scheduled appointments
   * - "Error deleting patient"
     - Database error

Implementation Details
======================

Patient Database Schema
-----------------------

.. code-block:: sql

    CREATE TABLE patients (
        patient_id INT PRIMARY KEY AUTO_INCREMENT,
        full_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        phone VARCHAR(20) UNIQUE,
        password VARCHAR(255),
        date_of_birth DATE,
        gender VARCHAR(20),
        address TEXT,
        city VARCHAR(50),
        state VARCHAR(50),
        postal_code VARCHAR(20),
        emergency_contact VARCHAR(100),
        emergency_phone VARCHAR(20),
        is_active TINYINT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        deleted_at TIMESTAMP NULL
    );

    CREATE INDEX idx_email ON patients(email);
    CREATE INDEX idx_phone ON patients(phone);
    CREATE INDEX idx_active ON patients(is_active);
    CREATE INDEX idx_created_at ON patients(created_at);

Validation Rules
----------------

**Full Name**
- Required
- 2-100 characters
- Letters and spaces only
- Trimmed of whitespace

**Email**
- Required
- Valid email format
- Unique (no duplicates)
- Case-insensitive

**Phone**
- Required
- Valid phone format
- Unique (no duplicates)
- Stored with formatting

**Date of Birth**
- Optional
- Valid date format (YYYY-MM-DD)
- Age 0-150 years
- Not in future

Gender
~~~~~~

- Optional
- Predefined options:
  - M (Male)
  - F (Female)
  - Other
  - Prefer not to say

Address
~~~~~~~

- Optional
- 0-200 characters
- Can include street, number

City, State, Postal Code
~~~~~~~~~~~~~~~~~~~~~~~~

- Optional
- City/State: 0-50 characters
- Postal Code: 0-20 characters

Emergency Contact
~~~~~~~~~~~~~~~~~~

- Optional
- 0-100 characters
- Must be person name if provided
- Phone: valid format if provided

Gender Options
---------------

Supported gender values:

- M - Male
- F - Female
- O - Other
- P - Prefer not to say
- (empty) - Not specified

Search and Filter
=================

Search Functionality
--------------------

Search can match on:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Field
     - Query Pattern
   * - Full Name
     - LIKE %search% (case-insensitive)
   * - Email
     - LIKE %search%
   * - Phone
     - LIKE %search% (searches numeric portion)

**Example Searches**

- "john" → Matches "John Smith", "Johnny Doe"
- "smith@" → Matches "john.smith@email.com"
- "555-01" → Matches "555-0100", "555-0123"

Filter by Status
----------------

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Status
     - SQL WHERE Clause
   * - active
     - is_active = 1
   * - inactive
     - is_active = 0
   * - all
     - (no filter)

Sort Options
------------

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Sort Option
     - SQL ORDER BY
   * - created_at (default)
     - ORDER BY created_at DESC
   * - name
     - ORDER BY full_name ASC
   * - email
     - ORDER BY email ASC
   * - updated_at
     - ORDER BY updated_at DESC

Pagination
----------

Default: 10 patients per page

.. code-block:: python

    per_page = 10
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * per_page
    

Code Examples
=============

List Patients (Python)
----------------------

.. code-block:: python

    import requests

    headers = {'Cookie': 'session=your_session_id'}
    response = requests.get(
        'http://localhost:5000/admin/patients',
        headers=headers,
        params={
            'search': 'smith',
            'page': 1,
            'status': 'active'
        }
    )

    if response.status_code == 200:
        print("Patient list retrieved")

Edit Patient (JavaScript)
--------------------------

.. code-block:: javascript

    const patientData = {
        full_name: 'Jane Smith',
        email: 'jane.smith@email.com',
        phone: '555-5555',
        date_of_birth: '1990-06-20',
        gender: 'F',
        address: '789 Pine Road',
        city: 'Portland',
        state: 'OR',
        postal_code: '97201',
        emergency_contact: 'John Smith',
        emergency_phone: '555-5550'
    };

    const formData = new FormData();
    Object.keys(patientData).forEach(key => {
        formData.append(key, patientData[key]);
    });

    fetch('/admin/patients/edit/42', {
        method: 'POST',
        body: formData,
        credentials: 'include'
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    });

Delete Patient (cURL)
---------------------

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/patients/delete/42 \
         -b "session=your_session_id" \
         -d "confirm=yes&reason=Patient%20requested%20account%20deletion"

Performance Optimization
========================

Database Indexes
----------------

For optimal query performance:

.. code-block:: sql

    CREATE INDEX idx_email ON patients(email);
    CREATE INDEX idx_phone ON patients(phone);
    CREATE INDEX idx_active ON patients(is_active);
    CREATE INDEX idx_created_at ON patients(created_at);
    CREATE INDEX idx_full_name ON patients(full_name);

Query Optimization
-------------------

- Filter by is_active = 1 for list views
- Paginate large result sets
- Use LIMIT to prevent large data transfers
- Index frequently searched fields

Patient Relationships
======================

Patient Associations
---------------------

Each patient can have:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Associated Data
     - Description
   * - Appointments
     - Multiple scheduled/completed appointments with doctors
   * - Medical Records
     - Medical history, diagnoses, treatments, prescriptions
   * - Prescriptions
     - Current and past medications
   * - Payments
     - Appointment fees, services charged

Patient Deletion Impact
------------------------

When a patient is soft-deleted:

- Appointments remain visible in history
- Medical records preserved for historical access
- Payment records kept for accounting
- Patient can be re-activated if needed

Restoring Deleted Patient
---------------------------

To restore a deleted patient:

.. code-block:: sql

    UPDATE patients
    SET is_active = 1,
        deleted_at = NULL
    WHERE patient_id = 42

Common Issues
=============

Email Already in Use
---------------------

**Problem**: Cannot edit - email already registered

**Solution**:
- Use different email address
- Check if duplicate patient exists
- Verify email not assigned to another patient

Duplicate Phone Number
----------------------

**Problem**: Cannot edit - phone in use

**Solution**:
- Verify phone number is correct
- Use different phone number
- Check for typos in entry

Cannot Delete Patient
---------------------

**Problem**: Delete fails - "active appointments"

**Solution**:
- Complete or cancel active appointments first
- Query: ``SELECT * FROM appointments WHERE patient_id=X AND status='scheduled'``
- Reschedule appointments to other dates

Invalid Date of Birth
----------------------

**Problem**: "Invalid date of birth" error

**Solution**:
- Use format: YYYY-MM-DD (e.g., 1985-03-15)
- Ensure date is not in future
- Verify patient age is realistic (0-150 years)
- Check for typos in year/month/day

Search Not Working
-------------------

**Problem**: Search returns no results

**Solution**:
- Check search term spelling
- Try partial name (e.g., "smith" instead of full name)
- Verify patients exist: ``SELECT COUNT(*) FROM patients WHERE is_active=1``
- Clear filter to search all statuses

Next Steps
==========

1. **View Patient Records** → Medical records through doctor interface
2. **Schedule Appointments** → Book appointments with doctors
3. **View Dashboard** → See system overview (see :doc:`admin_dashboard`)
4. **Manage Doctors** → View doctor information (see :doc:`doctor_management`)
5. **View API Endpoints** → See complete API reference (see :doc:`api_endpoints`)
6. **Troubleshoot Issues** → See common solutions (see :doc:`troubleshooting`)
