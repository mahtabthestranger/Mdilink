Routes (Controller)
===================

The controller handles HTTP requests and connects Model with View.

Location: ``Mahtabapp.py``

Patient Registration
--------------------

**URL:** ``/patient/register``

**Methods:** GET, POST

**Description:**

* GET - Display registration form
* POST - Process registration

**Flow:**

1. User fills registration form
2. Validate input data
3. Check if email exists
4. Hash password
5. Save to database
6. Redirect to login

Patient Login
-------------

**URL:** ``/patient/login``

**Methods:** GET, POST

**Description:**

* GET - Display login form
* POST - Authenticate user

**Flow:**

1. User enters email and password
2. Find patient by email
3. Verify password hash
4. Create session
5. Redirect to dashboard

Patient Dashboard
-----------------

**URL:** ``/patient/dashboard``

**Methods:** GET

**Description:**

Protected route - requires authentication.

**Flow:**

1. Check if user is logged in
2. If not, redirect to login
3. Display dashboard with user info

Logout
------

**URL:** ``/logout``

**Methods:** GET

**Description:**

Clears user session and redirects to login.

**Flow:**

1. Clear session data
2. Flash success message
3. Redirect to login page

