================================================================================
Admin Authentication - Login & Session Management
================================================================================

Authentication Overview
=======================

The admin authentication module provides secure login functionality and session
management for the Medilink administration system.

Admin Login Route
=================

**Endpoint**: ``/admin/login``

**Methods**: GET, POST

**Description**

Handles admin authentication by validating username and password credentials.
On successful authentication, creates a session for the admin user.

Request (GET)
-------------

Displays the admin login form.

.. code-block:: bash

    GET /admin/login
    Response: HTML login form

Request (POST)
--------------

Processes admin login credentials.

**Parameters**

.. list-table::
   :widths: 20 15 15 50
   :header-rows: 1

   * - Parameter
     - Type
     - Required
     - Description
   * - username
     - string
     - Yes
     - Admin username for authentication
   * - password
     - string
     - Yes
     - Admin password (will be verified against hash)

**Example Request**

.. code-block:: bash

    curl -X POST http://localhost:5000/admin/login \
         -d "username=admin&password=password123"

Response - Success (POST)
--------------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/dashboard

**Session Variables Set**

.. list-table::
   :widths: 20 50
   :header-rows: 1

   * - Variable
     - Description
   * - user_type
     - Set to 'admin'
   * - user_id
     - Admin ID from database
   * - user_name
     - Admin full name
   * - username
     - Admin username
   * - session.permanent
     - Set to True for persistent session

**Flash Message**

.. code-block:: text

    Welcome, [Admin Name]!

Response - Failure (POST)
--------------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/login

**Possible Error Messages**

.. list-table::
   :widths: 40 60
   :header-rows: 1

   * - Error
     - Cause
   * - "Please enter username and password"
     - Missing username or password
   * - "Invalid username or password"
     - Credentials don't match database
   * - "An error occurred during login. Please try again"
     - Database or server error

Response - Form Display (GET)
------------------------------

**Status Code**: 200 (OK)

**Content**: Rendered login form (admin/login.html)

**Form Fields**

- Username input field
- Password input field
- Submit button
- Remember me option (if implemented)

Implementation Details
======================

Authentication Flow
-------------------

.. code-block:: text

    1. User submits login form (POST)
           ↓
    2. Validate inputs not empty
           ↓
    3. Call Admin.verify_password()
           ↓
    4. Check credentials against database
           ↓
    5a. If valid:
        - Set session variables
        - Redirect to dashboard
           ↓
    5b. If invalid:
        - Show error message
        - Redirect to login

Code Example
~~~~~~~~~~~~

.. code-block:: python

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                flash('Please enter username and password', 'error')
                return redirect(url_for('admin_login'))

            try:
                admin = Admin.verify_password(mysql, username, password)

                if admin:
                    session['user_type'] = 'admin'
                    session['user_id'] = admin['admin_id']
                    session['user_name'] = admin['full_name']
                    session['username'] = admin['username']
                    session.permanent = True

                    flash(f'Welcome, {admin["full_name"]}!', 'success')
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid username or password', 'error')
                    return redirect(url_for('admin_login'))

            except Exception as error:
                print(f'Admin login error: {error}')
                flash('An error occurred during login', 'error')
                return redirect(url_for('admin_login'))

        return render_template('admin/login.html')

Session Management
==================

Session Variables
-----------------

The following variables are stored in the Flask session after login:

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Variable
     - Type
     - Purpose
   * - user_type
     - string
     - Type of user ('admin')
   * - user_id
     - integer
     - Unique admin identifier
   * - user_name
     - string
     - Display name for UI
   * - username
     - string
     - Login username
   * - permanent
     - boolean
     - Session persistence flag

Session Timeout
---------------

**Default Timeout**: 24 hours

**Configuration** (in config.py)

.. code-block:: python

    from datetime import timedelta

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['SESSION_COOKIE_SECURE'] = False 
    app.config['SESSION_COOKIE_HTTPONLY'] = True

Session Validation
------------------

All admin routes check the session before processing:

.. code-block:: python

    if session.get('user_type') != 'admin':
        flash('Please login as admin', 'error')
        return redirect(url_for('admin_login'))

Security Features
==================

Password Hashing
----------------

Passwords are stored as hashes using werkzeug.security:

.. code-block:: python

    from werkzeug.security import generate_password_hash, check_password_hash

    hashed = generate_password_hash(password, method='sha256')

    is_valid = check_password_hash(hashed, provided_password)

Input Validation
----------------

- **Username**: Required, trimmed of whitespace
- **Password**: Required, checked against hash
- **Empty Fields**: Rejected with error message

Error Handling
--------------

All exceptions are caught and logged:

.. code-block:: python

    try:
        admin = Admin.verify_password(mysql, username, password)
    except Exception as error:
        print(f'Admin login error: {error}')
        flash('An error occurred during login', 'error')

Database Query
--------------

The login process queries the admin table:

.. code-block:: sql

    SELECT admin_id, username, password, full_name
    FROM admins
    WHERE username = %s

Best Practices
==============

For Administrators
------------------

1. **Strong Passwords**
   - Use passwords with 12+ characters
   - Mix uppercase, lowercase, numbers, symbols
   - Avoid dictionary words

2. **Session Security**
   - Don't share admin credentials
   - Logout when finished
   - Clear browser cookies regularly

3. **Account Protection**
   - Change default password immediately
   - Review login history
   - Monitor for suspicious activity

For Developers
--------------

1. **Never Log Passwords**
   - Only log authentication events, not credentials
   - Log successful and failed attempts
   - Include timestamp and source IP

2. **Secure Storage**
   - Always hash passwords
   - Use strong hashing algorithm
   - Never store plaintext passwords

3. **Session Management**
   - Set session timeout appropriately
   - Implement logout functionality
   - Use secure cookies in production

4. **Error Messages**
   - Don't reveal if username or password is wrong
   - Use generic "Invalid credentials" message
   - Prevent username enumeration

Troubleshooting
===============

Login Not Working
-----------------

**Symptom**: Login fails even with correct credentials

**Solutions**:

1. Check database connection
2. Verify admin record exists: ``SELECT * FROM admins WHERE username='admin'``
3. Check password hash: Ensure password was hashed correctly
4. Review error logs for database errors

Session Expires
---------------

**Symptom**: Logged out unexpectedly

**Solutions**:

1. Check session timeout setting in config.py
2. Verify cookies are enabled in browser
3. Check if server was restarted (clears sessions)
4. Increase PERMANENT_SESSION_LIFETIME if needed

"Please login as admin" Error
------------------------------

**Symptom**: Always redirected to login

**Solutions**:

1. Login first
2. Check if session.permanent = True
3. Verify browser accepts cookies
4. Check if session variables are being set correctly

Default Credentials
===================

Default admin account (if created during initialization):

- **Username**: admin
- **Password**: password123 (should be changed!)

**Important**: Change default password immediately in production!

Next Steps
==========

1. After login, proceed to :doc:`admin_dashboard`
2. Manage doctors via :doc:`doctor_management`
3. Manage patients via :doc:`patient_management`
4. Reference :doc:`api_endpoints` for complete API
5. Check :doc:`troubleshooting` for common issues
