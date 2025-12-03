================================================================================
API Endpoints Reference - Complete Admin Routes
================================================================================

Complete API Reference
======================

This document provides a comprehensive reference for all admin API endpoints
in the Medilink system.

Authentication
===============

All admin endpoints require authentication. Admin must be logged in and have
an active session.

**Required Headers**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Header
     - Description
   * - Cookie
     - session=<session_id> (automatic in browser)
   * - Content-Type
     - application/x-www-form-urlencoded (for POST)

**Unauthorized Response**

.. code-block:: text

    Status: 302 Redirect
    Location: /admin/login
    Flash: "Please login as admin"

HTTP Status Codes
=================

.. list-table::
   :widths: 15 85
   :header-rows: 1

   * - Status
     - Meaning
   * - 200
     - Success - Page displayed or data returned
   * - 302
     - Redirect - After successful operation or authentication required
   * - 400
     - Bad Request - Invalid parameters or validation failed
   * - 404
     - Not Found - Resource (doctor/patient) not found
   * - 500
     - Server Error - Database or application error

Admin Endpoints Summary
=======================

.. list-table::
   :widths: 25 12 20 43
   :header-rows: 1

   * - Endpoint
     - Method
     - Auth
     - Purpose
   * - /admin/login
     - GET, POST
     - No
     - Admin authentication
   * - /admin/dashboard
     - GET
     - Yes
     - System statistics & overview
   * - /admin/doctors
     - GET
     - Yes
     - List all active doctors
   * - /admin/doctors/add
     - GET, POST
     - Yes
     - Create new doctor
   * - /admin/doctors/edit/<id>
     - GET, POST
     - Yes
     - Update doctor information
   * - /admin/doctors/delete/<id>
     - POST
     - Yes
     - Delete/deactivate doctor
   * - /admin/patients
     - GET
     - Yes
     - List all active patients
   * - /admin/patients/edit/<id>
     - GET, POST
     - Yes
     - Update patient information
   * - /admin/patients/delete/<id>
     - POST
     - Yes
     - Delete/deactivate patient

Detailed Endpoints
==================

1. Admin Login
--------------

**POST /admin/login**

Authenticate admin with username and password.

**Request**

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/login \
         -d "username=admin&password=password123"

**Request Parameters**

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Parameter
     - Required
     - Description
   * - username
     - Yes
     - Admin username
   * - password
     - Yes
     - Admin password (plaintext, hashed on server)

**Response - Success (302)**

.. code-block:: text

    Location: /admin/dashboard
    Set-Cookie: session=<session_id>
    Flash: "Welcome, [Admin Name]!"

**Response - Failure (302)**

.. code-block:: text

    Location: /admin/login
    Flash: "Invalid username or password"

**See Also**: :doc:`admin_authentication`

2. Admin Dashboard
------------------

**GET /admin/dashboard**

Retrieve admin dashboard with system statistics.

**Request**

.. code-block:: bash

    curl -X GET http://localhost:5000/admin/dashboard \
         -b "session=<session_id>"

**Response - Success (200)**

.. code-block:: text

    Content-Type: text/html
    Body: Rendered dashboard HTML with:
      - Total doctors count
      - Total patients count
      - Total appointments count
      - Pending appointments count
      - System status
      - Quick action links

**Response - Unauthorized (302)**

.. code-block:: text

    Location: /admin/login
    Flash: "Please login as admin"

**See Also**: :doc:`admin_dashboard`

3. List Doctors
---------------

**GET /admin/doctors**

Retrieve paginated list of all active doctors.

**Request**

.. code-block:: bash

    curl -X GET "http://localhost:5000/admin/doctors?search=cardio&page=1" \
         -b "session=<session_id>"

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
     - Search by name or specialty
   * - page
     - integer
     - 1
     - Page number for pagination
   * - specialty
     - string
     - (all)
     - Filter by specialty

**Response - Success (200)**

.. code-block:: text

    Content-Type: text/html
    Body: Rendered doctors list with:
      - List of 10 doctors per page
      - Pagination controls
      - Search/filter options
      - Add/Edit/Delete buttons

**Response - Unauthorized (302)**

.. code-block:: text

    Location: /admin/login

**See Also**: :doc:`doctor_management`

4. Add Doctor
-------------

**GET /admin/doctors/add**

Display form to add new doctor.

**Request**

.. code-block:: bash

    curl -X GET http://localhost:5000/admin/doctors/add \
         -b "session=<session_id>"

**Response - Success (200)**

.. code-block:: text

    Content-Type: text/html
    Body: Rendered add doctor form with fields:
      - Full Name
      - Specialty (dropdown)
      - Phone
      - Email
      - Experience (years)
      - License Number
      - Password
      - Submit button

**POST /admin/doctors/add**

Submit new doctor information.

**Request**

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/doctors/add \
         -b "session=<session_id>" \
         -d "full_name=Dr.%20John%20Smith&specialty=Cardiology&phone=555-0100&\
             email=john@medilink.com&experience=10&license_number=MD123456&\
             password=SecurePassword123"

**Request Parameters**

.. list-table::
   :widths: 18 12 15 55
   :header-rows: 1

   * - Parameter
     - Required
     - Type
     - Description
   * - full_name
     - Yes
     - string
     - Doctor's full name (2-100 chars)
   * - specialty
     - Yes
     - string
     - Medical specialty (from list)
   * - phone
     - Yes
     - string
     - Phone number (must be unique)
   * - email
     - Yes
     - string
     - Email address (must be unique)
   * - experience
     - No
     - integer
     - Years of experience
   * - license_number
     - Yes
     - string
     - Medical license number (unique)
   * - password
     - Yes
     - string
     - Login password (8+ chars)

**Response - Success (302)**

.. code-block:: text

    Location: /admin/doctors
    Flash: "Doctor added successfully!"

**Response - Validation Error (200)**

.. code-block:: text

    Content-Type: text/html
    Body: Re-rendered form with error messages
    Flash: Error message (e.g., "Email already exists")

**Response - Server Error (302)**

.. code-block:: text

    Location: /admin/doctors/add
    Flash: "Error adding doctor. Please try again"

**See Also**: :doc:`doctor_management`

5. Edit Doctor
--------------

**GET /admin/doctors/edit/<id>**

Display form to edit doctor information.

**Request**

.. code-block:: bash

    curl -X GET http://localhost:5000/admin/doctors/edit/5 \
         -b "session=<session_id>"

**URL Parameters**

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - id
     - integer
     - Doctor ID to edit

**Response - Success (200)**

.. code-block:: text

    Content-Type: text/html
    Body: Pre-filled edit form with current doctor data

**Response - Not Found (302)**

.. code-block:: text

    Location: /admin/doctors
    Flash: "Doctor not found"

**POST /admin/doctors/edit/<id>**

Submit updated doctor information.

**Request**

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/doctors/edit/5 \
         -b "session=<session_id>" \
         -d "full_name=Dr.%20John%20Anderson&specialty=Neurology&\
             phone=555-9876&email=john.a@medilink.com&experience=12"

**Request Parameters**

Same as Add Doctor, but password is optional (omit to keep current).

**Response - Success (302)**

.. code-block:: text

    Location: /admin/doctors
    Flash: "Doctor updated successfully!"

**Response - Validation Error (200)**

.. code-block:: text

    Body: Re-rendered form with error messages

**See Also**: :doc:`doctor_management`

6. Delete Doctor
----------------

**POST /admin/doctors/delete/<id>**

Delete (soft-delete) a doctor.

**Request**

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/doctors/delete/5 \
         -b "session=<session_id>" \
         -d "confirm=yes"

**URL Parameters**

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - id
     - integer
     - Doctor ID to delete

**Request Parameters**

.. list-table::
   :widths: 15 15 70
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - confirm
     - string
     - "yes" to confirm deletion

**Response - Success (302)**

.. code-block:: text

    Location: /admin/doctors
    Flash: "Doctor deleted successfully"

**Response - Not Found (302)**

.. code-block:: text

    Location: /admin/doctors
    Flash: "Doctor not found"

**Response - Active Appointments (302)**

.. code-block:: text

    Location: /admin/doctors
    Flash: "Cannot delete - doctor has active appointments"

**See Also**: :doc:`doctor_management`

7. List Patients
----------------

**GET /admin/patients**

Retrieve paginated list of all active patients.

**Request**

.. code-block:: bash

    curl -X GET "http://localhost:5000/admin/patients?search=smith&page=1" \
         -b "session=<session_id>"

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
     - Search by name, email, phone
   * - page
     - integer
     - 1
     - Page number for pagination
   * - status
     - string
     - active
     - Filter (active, inactive, all)

**Response - Success (200)**

.. code-block:: text

    Content-Type: text/html
    Body: Rendered patients list with:
      - List of up to 10 patients
      - Patient names, emails, phone numbers
      - Pagination controls
      - Edit/Delete buttons

**See Also**: :doc:`patient_management`

8. Edit Patient
---------------

**GET /admin/patients/edit/<id>**

Display form to edit patient information.

**Request**

.. code-block:: bash

    curl -X GET http://localhost:5000/admin/patients/edit/42 \
         -b "session=<session_id>"

**Response - Success (200)**

.. code-block:: text

    Content-Type: text/html
    Body: Pre-filled edit form with current patient data

**POST /admin/patients/edit/<id>**

Submit updated patient information.

**Request**

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/patients/edit/42 \
         -b "session=<session_id>" \
         -d "full_name=John%20Anderson&email=john.a@email.com&phone=555-4321&\
             date_of_birth=1985-03-15&gender=M"

**Request Parameters**

.. list-table::
   :widths: 18 12 15 55
   :header-rows: 1

   * - Parameter
     - Required
     - Type
     - Description
   * - full_name
     - Yes
     - string
     - Patient's full name
   * - email
     - Yes
     - string
     - Email address (unique)
   * - phone
     - Yes
     - string
     - Phone number (unique)
   * - date_of_birth
     - No
     - date
     - YYYY-MM-DD format
   * - gender
     - No
     - string
     - M, F, Other, Prefer not to say
   * - address
     - No
     - string
     - Street address
   * - city
     - No
     - string
     - City name
   * - state
     - No
     - string
     - State/Province
   * - postal_code
     - No
     - string
     - Postal code
   * - emergency_contact
     - No
     - string
     - Emergency contact name
   * - emergency_phone
     - No
     - string
     - Emergency contact phone

**Response - Success (302)**

.. code-block:: text

    Location: /admin/patients
    Flash: "Patient updated successfully!"

**See Also**: :doc:`patient_management`

9. Delete Patient
-----------------

**POST /admin/patients/delete/<id>**

Delete (soft-delete) a patient.

**Request**

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/patients/delete/42 \
         -b "session=<session_id>" \
         -d "confirm=yes"

**Response - Success (302)**

.. code-block:: text

    Location: /admin/patients
    Flash: "Patient deleted successfully"

**Response - Active Appointments (302)**

.. code-block:: text

    Location: /admin/patients
    Flash: "Cannot delete - patient has active appointments"

**See Also**: :doc:`patient_management`

Error Codes Summary
===================

Authentication Errors
---------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Message
     - Cause & Solution
   * - "Please login as admin"
     - Not authenticated. Login first via /admin/login
   * - "Invalid username or password"
     - Wrong credentials. Verify username and password are correct
   * - "An error occurred during login"
     - Server/database error. Check server logs

Validation Errors
-----------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Message
     - Cause & Solution
   * - "Full name is required"
     - Missing required field. Enter full name
   * - "Invalid email format"
     - Email format incorrect. Use: user@domain.com
   * - "Email already exists"
     - Email in use. Use different email address
   * - "Phone already in use"
     - Phone assigned to another user. Use different phone
   * - "Invalid date of birth"
     - Date format or age invalid. Use YYYY-MM-DD format
   * - "Password must be 8+ characters"
     - Password too short. Use 8 or more characters

Resource Errors
---------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Message
     - Cause & Solution
   * - "Doctor not found"
     - Invalid doctor ID. Verify doctor exists
   * - "Patient not found"
     - Invalid patient ID. Verify patient exists
   * - "Cannot delete - active appointments"
     - Has scheduled appointments. Complete/cancel first

Server Errors
-------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Error Message
     - Cause & Solution
   * - "Error adding doctor"
     - Database error. Check database logs
   * - "Error loading dashboard"
     - Database connection issue. Verify MySQL running
   * - "An error occurred"
     - Server error. Check application error logs

Common Response Patterns
========================

Successful Form Submission
---------------------------

.. code-block:: text

    POST request to form endpoint
    ↓
    Validation on server
    ↓
    If valid: Database update → 302 redirect with success flash
    ↓
    If invalid: 200 response with re-rendered form showing errors

List/Read Operations
---------------------

.. code-block:: text

    GET request
    ↓
    Check authentication
    ↓
    Query database
    ↓
    200 response with rendered HTML template

Deletion Operations
-------------------

.. code-block:: text

    POST request with confirm=yes
    ↓
    Check authentication
    ↓
    Verify resource exists
    ↓
    Check for constraints (active appointments, etc.)
    ↓
    If allowed: Soft delete → 302 redirect
    ↓
    If not allowed: 302 redirect with error message

API Usage Tips
==============

Browser-Based Requests
-----------------------

When accessing from browser:

1. Login first: Navigate to /admin/login
2. Enter credentials
3. Automatic session cookie set
4. Access protected endpoints

cURL Requests
-------------

.. code-block:: bash

    curl -c cookies.txt -X POST http://localhost:5000/admin/login \
         -d "username=admin&password=password123"

    curl -b cookies.txt -X GET http://localhost:5000/admin/dashboard

JavaScript Fetch
----------------

.. code-block:: javascript

    fetch('/admin/doctors', {
        method: 'GET',
        credentials: 'include'  
    })
    .then(response => response.text())
    .then(html => console.log(html));

Pagination Example
------------------

.. code-block:: javascript

    fetch('/admin/doctors?page=2', {
        credentials: 'include'
    })
    .then(response => response.text());

Related Documentation
=====================

- :doc:`admin_authentication` - Login & session management
- :doc:`admin_dashboard` - Dashboard statistics
- :doc:`doctor_management` - Doctor CRUD operations
- :doc:`patient_management` - Patient CRUD operations
- :doc:`examples` - Code examples for common tasks
- :doc:`troubleshooting` - Solutions for common issues
