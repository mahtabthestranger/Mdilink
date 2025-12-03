================================================================================
Doctor Management - CRUD Operations
================================================================================

Doctor Management Overview
===========================

The doctor management module provides complete CRUD (Create, Read, Update, 
Delete) operations for managing doctors in the Medilink system.

Route Summary
=============

.. list-table::
   :widths: 25 15 15 45
   :header-rows: 1

   * - Route
     - Method
     - Auth
     - Description
   * - /admin/doctors
     - GET
     - Admin
     - List all active doctors
   * - /admin/doctors/add
     - GET, POST
     - Admin
     - Add new doctor
   * - /admin/doctors/edit/<id>
     - GET, POST
     - Admin
     - Edit existing doctor
   * - /admin/doctors/delete/<id>
     - POST
     - Admin
     - Delete/deactivate doctor

List Doctors
============

**Endpoint**: ``/admin/doctors``

**Methods**: GET

**Description**

Displays a paginated list of all active doctors with search and filter options.

Request
-------

.. code-block:: bash

    GET /admin/doctors
    GET /admin/doctors?search=cardiac&page=1

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
     - Search doctors by name, specialty
   * - page
     - integer
     - 1
     - Page number for pagination
   * - specialty
     - string
     - (all)
     - Filter by specialty (Cardiology, etc.)

Response - Success
------------------

**Status Code**: 200 (OK)

**Content-Type**: text/html

**Rendered Template**: admin/doctors.html

**Response Data**

.. code-block:: python

    {
        'doctors': [
            {
                'doctor_id': 1,
                'full_name': 'Dr. John Smith',
                'specialty': 'Cardiology',
                'phone': '555-0100',
                'email': 'john.smith@medilink.com',
                'experience': 10,
                'is_active': 1,
                'created_at': '2023-01-15 08:30:00'
            },
        ],
        'total_count': 15,
        'page': 1,
        'per_page': 10,
        'total_pages': 2
    }

Database Query
--------------

.. code-block:: sql

    SELECT * FROM doctors
    WHERE is_active = 1
    AND (full_name LIKE %search% OR specialty LIKE %search%)
    ORDER BY created_at DESC
    LIMIT 10 OFFSET 0

Add Doctor
==========

**Endpoint**: ``/admin/doctors/add``

**Methods**: GET, POST

**Description**

Form to add a new doctor to the system.

Request (GET)
-------------

.. code-block:: bash

    GET /admin/doctors/add

Response (GET)
~~~~~~~~~~~~~~

**Status Code**: 200 (OK)

**Content**: Rendered add doctor form (admin/add_doctor.html)

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
     - 2-100 characters, letters/spaces only
   * - specialty
     - select
     - Yes
     - From predefined list
   * - phone
     - tel
     - Yes
     - Valid phone format (555-XXXX or similar)
   * - email
     - email
     - Yes
     - Valid email format, unique
   * - experience
     - number
     - No
     - 0-70 years
   * - bio
     - textarea
     - No
     - 0-500 characters
   * - license_number
     - text
     - Yes
     - Unique license ID
   * - password
     - password
     - Yes
     - 8+ characters

Request (POST)
--------------

.. code-block:: bash

    POST /admin/doctors/add
    Content-Type: application/x-www-form-urlencoded

    full_name=Dr.%20Sarah%20Johnson&specialty=Cardiology&phone=555-0123&
    email=sarah@medilink.com&experience=8&license_number=MD123456

**Request Parameters**

All parameters listed in form fields table above.

Response (POST) - Success
--------------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/doctors

**Flash Message**: "Doctor added successfully!"

**Database Changes**

New row inserted into doctors table:

.. code-block:: sql

    INSERT INTO doctors (
        full_name, specialty, phone, email, experience,
        bio, license_number, password, is_active, created_at
    ) VALUES (
        'Dr. Sarah Johnson', 'Cardiology', '555-0123', 
        'sarah@medilink.com', 8, '', 'MD123456', 
        <hashed_password>, 1, NOW()
    )

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
   * - "Email already exists"
     - Email already registered
   * - "Phone number already exists"
     - Phone already registered
   * - "Password must be at least 8 characters"
     - Password too short
   * - "Specialty is required"
     - Specialty not selected
   * - "License number already exists"
     - Duplicate license number

Response (POST) - Server Error
-------------------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/doctors/add

**Flash Message**: "Error adding doctor. Please try again"

Edit Doctor
===========

**Endpoint**: ``/admin/doctors/edit/<id>``

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
     - Doctor ID to edit

**Description**

Form to edit an existing doctor's information.

Request (GET)
-------------

.. code-block:: bash

    GET /admin/doctors/edit/5

Response (GET)
~~~~~~~~~~~~~~

**Status Code**: 200 (OK)

**Content**: Pre-filled edit form with doctor data

**Form Fields**

Same as add doctor, but pre-populated with existing data.

**Note**: Password field optional on edit (leave empty to keep current)

Request (POST)
--------------

.. code-block:: bash

    POST /admin/doctors/edit/5
    Content-Type: application/x-www-form-urlencoded

    full_name=Dr.%20Sarah%20Anderson&specialty=Neurology&
    phone=555-9876&email=sarah.a@medilink.com&experience=10

Response (POST) - Success
--------------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/doctors

**Flash Message**: "Doctor updated successfully!"

**Database Changes**

.. code-block:: sql

    UPDATE doctors
    SET full_name = 'Dr. Sarah Anderson',
        specialty = 'Neurology',
        phone = '555-9876',
        email = 'sarah.a@medilink.com',
        experience = 10
    WHERE doctor_id = 5

Response (POST) - Errors
------------------------

Same validation errors as add doctor.

**Additional Errors**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error
     - Cause
   * - "Doctor not found"
     - Invalid doctor ID
   * - "Email already in use"
     - Email assigned to another doctor
   * - "Phone already in use"
     - Phone assigned to another doctor

Delete Doctor
=============

**Endpoint**: ``/admin/doctors/delete/<id>``

**Methods**: POST

**Description**

Soft-delete (deactivate) a doctor. Data is preserved in database.

Request
-------

.. code-block:: bash

    POST /admin/doctors/delete/5

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

Response - Success
------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/doctors

**Flash Message**: "Doctor deleted successfully"

**Database Changes**

Soft delete (mark inactive):

.. code-block:: sql

    UPDATE doctors
    SET is_active = 0
    WHERE doctor_id = 5

Response - Error
----------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/doctors

**Flash Message**: "Doctor not found"

**Possible Errors**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error
     - Cause
   * - "Doctor not found"
     - Invalid doctor ID
   * - "Cannot delete - active appointments"
     - Doctor has scheduled appointments
   * - "Error deleting doctor"
     - Database error

Implementation Details
======================

Specialty List
--------------

Supported specialties:

- Cardiology
- Neurology
- Dermatology
- Orthopedics
- Pediatrics
- Psychiatry
- Ophthalmology
- General Practice
- Internal Medicine
- Surgery

Doctor Database Schema
----------------------

.. code-block:: sql

    CREATE TABLE doctors (
        doctor_id INT PRIMARY KEY AUTO_INCREMENT,
        full_name VARCHAR(100) NOT NULL,
        specialty VARCHAR(50) NOT NULL,
        phone VARCHAR(20) UNIQUE,
        email VARCHAR(100) UNIQUE,
        experience INT DEFAULT 0,
        bio TEXT,
        license_number VARCHAR(50) UNIQUE,
        password VARCHAR(255),
        is_active TINYINT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

    CREATE INDEX idx_email ON doctors(email);
    CREATE INDEX idx_phone ON doctors(phone);
    CREATE INDEX idx_specialty ON doctors(specialty);
    CREATE INDEX idx_active ON doctors(is_active);

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
- Unique across doctors table
- Case-insensitive comparison

**Phone**
- Required
- Valid phone format
- Unique across doctors table
- Stored with formatting

**Specialty**
- Required
- Must be from predefined list
- Case-sensitive exact match

**Experience**
- Optional
- 0-70 range
- Integer only

**License Number**
- Required
- Unique across system
- Used for verification

**Password** (on add)
- Required, minimum 8 characters
- Hashed using werkzeug.security
- Optional on update (leave to keep existing)

Code Examples
=============

List Doctors (Python)
---------------------

.. code-block:: python

    import requests

    headers = {'Cookie': 'session=your_session_id'}
    response = requests.get(
        'http://localhost:5000/admin/doctors',
        headers=headers,
        params={'search': 'cardio', 'page': 1}
    )

    if response.status_code == 200:
        doctors = response.html  

Add Doctor (JavaScript)
-----------------------

.. code-block:: javascript

    const formData = new FormData();
    formData.append('full_name', 'Dr. Michael Chen');
    formData.append('specialty', 'Orthopedics');
    formData.append('phone', '555-7890');
    formData.append('email', 'michael.chen@medilink.com');
    formData.append('experience', 12);
    formData.append('license_number', 'MD987654');
    formData.append('password', 'SecurePassword123');

    fetch('/admin/doctors/add', {
        method: 'POST',
        body: formData,
        credentials: 'include'  
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        }
    });

Delete Doctor (cURL)
--------------------

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/doctors/delete/5 \
         -b "session=your_session_id" \
         -d "confirm=yes"

Performance Optimization
========================

Database Indexes
----------------

For optimal query performance:

.. code-block:: sql

    CREATE INDEX idx_email ON doctors(email);
    CREATE INDEX idx_phone ON doctors(phone);
    CREATE INDEX idx_specialty ON doctors(specialty);
    CREATE INDEX idx_active ON doctors(is_active);
    CREATE INDEX idx_created_at ON doctors(created_at);

Query Optimization
-------------------

- Use SELECT * only when needed
- Filter by is_active = 1 for list views
- Paginate large result sets
- Cache frequently accessed specialties

Pagination
----------

Default: 10 doctors per page

.. code-block:: python

    per_page = 10
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * per_page
    

Common Issues
=============

Email Already Exists
---------------------

**Problem**: Cannot add doctor - email in use

**Solution**:
- Check if doctor already registered: ``SELECT * FROM doctors WHERE email='email@domain.com'``
- Use different email address
- Restore deleted doctor if needed

Duplicate Phone Number
----------------------

**Problem**: Phone number already registered

**Solution**:
- Verify phone number
- Use different phone
- Check for typos in entry

Cannot Delete Doctor
---------------------

**Problem**: Delete fails with "active appointments"

**Solution**:
- Complete or cancel active appointments first
- Check: ``SELECT * FROM appointments WHERE doctor_id=X AND status='scheduled'``

Search Not Working
-------------------

**Problem**: Search returns no results

**Solution**:
- Check search term spelling
- Verify doctors exist: ``SELECT * FROM doctors WHERE is_active=1``
- Try simpler search term
- Check database indexes

Next Steps
==========

1. **View Dashboard** → See :doc:`admin_dashboard`
2. **Manage Patients** → See :doc:`patient_management`
3. **Schedule Appointments** → See :doc:`api_endpoints`
4. **View System Status** → See :doc:`overview`
5. **Troubleshoot Issues** → See :doc:`troubleshooting`
