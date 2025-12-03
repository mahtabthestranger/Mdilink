================================================================================
Troubleshooting - Common Issues & Solutions
================================================================================

Troubleshooting Guide
=====================

This guide provides solutions for common issues encountered when using the
Medilink admin system.

Authentication Issues
=====================

Cannot Login
------------

**Symptom**: Login fails with "Invalid username or password"

**Possible Causes**:

1. Incorrect credentials
2. Admin account not created
3. Password changed/reset
4. Database connection issue
5. Admin account deactivated

**Solutions**:

1. **Verify credentials**
   - Confirm username and password are correct
   - Check for typos (case-sensitive)
   - Verify CAPS LOCK is off

2. **Check if admin exists**
   
   Connect to MySQL and check:

   .. code-block:: sql

       SELECT * FROM admins WHERE username='admin';

   If no results, create default admin:

   .. code-block:: sql

       INSERT INTO admins (username, password, full_name)
       VALUES ('admin', 'hashed_password_here', 'Administrator');

3. **Verify database connection**

   In Python shell:

   .. code-block:: python

       from flask_mysqldb import MySQL
       # Connection test in config

4. **Check admin account status**
   
   Ensure is_active = 1:

   .. code-block:: sql

       SELECT is_active FROM admins WHERE username='admin';

Session Expires
---------------

**Symptom**: Logged out unexpectedly, redirected to login page

**Possible Causes**:

1. Session timeout (default 24 hours)
2. Server restart
3. Browser cookies disabled
4. Browser session cleared

**Solutions**:

1. **Increase session timeout** (app.py or config.py)

   .. code-block:: python

       from datetime import timedelta
       app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=48)

2. **Enable cookies** in browser
   - Chrome: Settings → Privacy and security → Cookies
   - Firefox: Preferences → Privacy → Cookies

3. **Check session settings**

   .. code-block:: python

       app.config['SESSION_COOKIE_SECURE'] = False  # True in production
       app.config['SESSION_COOKIE_HTTPONLY'] = True
       app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

"Please Login As Admin" Error
------------------------------

**Symptom**: Always redirected to login, even after login

**Possible Causes**:

1. Session variables not set
2. Browser cookies not saved
3. Session not marked as permanent
4. user_type not in session

**Solutions**:

1. **Verify session variables** (in Python)

   .. code-block:: python

       @app.route('/debug/session')
       def debug_session():
           return {
               'user_type': session.get('user_type'),
               'user_id': session.get('user_id'),
               'permanent': session.permanent
           }

2. **Check login code** sets session properly

   .. code-block:: python

       session['user_type'] = 'admin'
       session.permanent = True  # Must be set

3. **Clear browser cookies** and login again
   - Right-click → Inspect → Application → Cookies
   - Delete session cookie
   - Re-login

Dashboard Issues
================

Dashboard Won't Load
--------------------

**Symptom**: Blank page or "Error loading dashboard"

**Possible Causes**:

1. Database connection issue
2. Tables don't exist
3. Query syntax error
4. Insufficient permissions

**Solutions**:

1. **Verify MySQL is running**

   .. code-block:: bash

       # Check if MySQL running
       mysqld --version
       # Or check via system services

2. **Check tables exist**

   .. code-block:: sql

       SHOW TABLES LIKE '%';
       -- Should show: admins, doctors, patients, appointments, etc.

3. **Verify data in tables**

   .. code-block:: sql

       SELECT COUNT(*) FROM doctors WHERE is_active = 1;
       SELECT COUNT(*) FROM patients WHERE is_active = 1;

4. **Check database permissions**

   Ensure user has SELECT permissions:

   .. code-block:: sql

       GRANT SELECT ON medilink.* TO 'medilink_user'@'localhost';

5. **Review error logs**

   Check app.py error output:

   .. code-block:: python

       except Exception as error:
           print(f'Dashboard error: {error}')  # See this error

Statistics Show Zero
--------------------

**Symptom**: All counts show 0

**Possible Causes**:

1. No data in tables
2. All records marked inactive (is_active = 0)
3. WHERE clause filtering out all results
4. Database query error

**Solutions**:

1. **Check for data**

   .. code-block:: sql

       SELECT COUNT(*) FROM doctors;
       -- If 0, no doctors created yet

2. **Check active flag**

   .. code-block:: sql

       SELECT COUNT(*) FROM doctors WHERE is_active = 0;
       -- If high number, records are inactive

3. **Reactivate records** if needed

   .. code-block:: sql

       UPDATE doctors SET is_active = 1 WHERE is_active = 0;

4. **Add test data**

   .. code-block:: sql

       INSERT INTO doctors (full_name, specialty, phone, email, 
                           license_number, is_active)
       VALUES ('Dr. Test', 'Cardiology', '555-0000', 
              'test@medilink.com', 'MD000', 1);

Slow Dashboard Load
-------------------

**Symptom**: Dashboard takes 5+ seconds to load

**Possible Causes**:

1. Large number of records (thousands+)
2. Missing database indexes
3. Slow database server
4. Network latency

**Solutions**:

1. **Add database indexes**

   .. code-block:: sql

       CREATE INDEX idx_doctors_active ON doctors(is_active);
       CREATE INDEX idx_patients_active ON patients(is_active);
       CREATE INDEX idx_appointments ON appointments(status);

2. **Check query performance** with EXPLAIN

   .. code-block:: sql

       EXPLAIN SELECT COUNT(*) FROM doctors WHERE is_active = 1;
       -- Check if using index

3. **Monitor database** during load

   MySQL workbench or command line:

   .. code-block:: bash

       mysqldump --single-transaction > backup.sql

4. **Implement caching** (advanced)

   .. code-block:: python

       from flask_caching import Cache
       cache = Cache(app, config={'CACHE_TYPE': 'simple'})

       @app.route('/admin/dashboard')
       @cache.cached(timeout=300)
       def admin_dashboard():
           # Dashboard logic

Doctor Management Issues
========================

Cannot Add Doctor
-----------------

**Symptom**: Form submission fails or redirects to same page

**Possible Causes**:

1. Validation error
2. Email/phone already exists
3. Required field missing
4. Database error

**Solutions**:

1. **Check form fields**
   - Ensure all required fields filled
   - Full Name: 2-100 characters
   - Email: valid format (user@domain.com)
   - Phone: valid format
   - Specialty: from dropdown list
   - License: unique value

2. **Check for duplicates**

   .. code-block:: sql

       SELECT * FROM doctors WHERE email='test@medilink.com';
       SELECT * FROM doctors WHERE phone='555-0000';
       SELECT * FROM doctors WHERE license_number='MD123';

3. **Check database constraints**

   .. code-block:: sql

       SHOW CREATE TABLE doctors\G
       -- Look for UNIQUE constraints

4. **Check error message** in browser
   - Look at form for error display
   - Check browser console (F12)

Email Already Exists
---------------------

**Symptom**: "Email already in use" error

**Possible Causes**:

1. Email assigned to another doctor
2. Soft-deleted doctor still in database
3. Duplicate entry error

**Solutions**:

1. **Find duplicate email**

   .. code-block:: sql

       SELECT * FROM doctors WHERE email='test@medilink.com';

2. **If soft-deleted doctor**

   .. code-block:: sql

       UPDATE doctors 
       SET is_active = 0 
       WHERE email='old@medilink.com'

3. **Or use different email**
   - Add suffix: test+1@medilink.com
   - Use different domain

Duplicate Phone Number
----------------------

**Symptom**: "Phone already in use" error

**Solutions**:

1. **Find duplicate phone**

   .. code-block:: sql

       SELECT * FROM doctors WHERE phone='555-0000';

2. **Use different phone** or remove from other record

Cannot Edit Doctor
-------------------

**Symptom**: Edit form won't submit or shows errors

**Possible Causes**:

1. Doctor ID not found
2. Validation error on new values
3. Email/phone conflict with another doctor
4. Database error

**Solutions**:

1. **Verify doctor exists**

   .. code-block:: sql

       SELECT * FROM doctors WHERE doctor_id=5;

2. **Check for email conflicts**

   .. code-block:: sql

       SELECT * FROM doctors 
       WHERE email='new@email.com' AND doctor_id != 5;

3. **Review error messages** in form

Cannot Delete Doctor
---------------------

**Symptom**: Delete fails with error message

**Possible Causes**:

1. Doctor has active appointments
2. Doctor ID not found
3. Database error

**Solutions**:

1. **Check active appointments**

   .. code-block:: sql

       SELECT * FROM appointments 
       WHERE doctor_id=5 AND status='scheduled';

2. **Complete appointments first**
   - Mark as completed in appointments table
   - Or reschedule to different doctor

3. **Check if doctor exists**

   .. code-block:: sql

       SELECT * FROM doctors WHERE doctor_id=5;

Doctor Search Not Working
--------------------------

**Symptom**: Search returns no results

**Solutions**:

1. **Try simpler search terms**
   - Instead of full name, try last name
   - Instead of specialty name, try partial

2. **Check if doctors exist**

   .. code-block:: sql

       SELECT * FROM doctors WHERE is_active=1 LIMIT 5;

3. **Try without filters**
   - Remove specialty filter
   - Check "All" pages option

Patient Management Issues
=========================

Cannot Edit Patient
--------------------

**Symptom**: Patient edit form won't submit

**Possible Causes**:

1. Validation errors
2. Email/phone already in use
3. Invalid date of birth
4. Database error

**Solutions**:

1. **Check form validation**
   - Full name: required, 2-100 chars
   - Email: required, valid format
   - Phone: required, unique
   - DOB: optional, valid date

2. **Verify email unique**

   .. code-block:: sql

       SELECT * FROM patients WHERE email='test@email.com';

3. **Check date format**
   - Use YYYY-MM-DD (e.g., 1985-03-15)
   - Cannot be future date
   - Age must be 0-150 years

Invalid Date of Birth
---------------------

**Symptom**: "Invalid date of birth" error

**Possible Causes**:

1. Wrong date format
2. Date in future
3. Age outside valid range

**Solutions**:

1. **Use correct format**: YYYY-MM-DD
   - Good: 1985-03-15
   - Bad: 03/15/1985 or 15-03-1985

2. **Verify not future date**
   - Don't enter dates after today

3. **Ensure realistic age**
   - Minimum: 0 years old
   - Maximum: 150 years old

Cannot Delete Patient
---------------------

**Symptom**: Delete fails with error

**Possible Causes**:

1. Active appointments exist
2. Patient ID not found

**Solutions**:

1. **Check appointments**

   .. code-block:: sql

       SELECT * FROM appointments 
       WHERE patient_id=42 AND status='scheduled';

2. **Complete appointments first**
   - Mark as completed or cancelled
   - Then try deleting patient

Search Not Working
-------------------

**Symptom**: Search finds nothing

**Solutions**:

1. **Try different search terms**
2. **Check database has data**

   .. code-block:: sql

       SELECT COUNT(*) FROM patients WHERE is_active=1;

3. **Search by parts**
   - Search first name
   - Search last name
   - Search email separately

Database Issues
===============

Cannot Connect to Database
---------------------------

**Symptom**: "Error loading dashboard" or "Database connection failed"

**Possible Causes**:

1. MySQL not running
2. Credentials wrong
3. Host unreachable
4. Database doesn't exist

**Solutions**:

1. **Check MySQL is running**

   .. code-block:: bash

       # Linux/Mac
       sudo service mysql status
       
       # Windows
       net start MySQL80  # or your version

2. **Test connection**

   .. code-block:: python

       import pymysql
       conn = pymysql.connect(
           host='localhost',
           user='root',
           password='password',
           database='medilink'
       )

3. **Verify credentials** in config.py

   .. code-block:: python

       app.config['MYSQL_HOST'] = 'localhost'
       app.config['MYSQL_USER'] = 'root'
       app.config['MYSQL_PASSWORD'] = 'your_password'
       app.config['MYSQL_DB'] = 'medilink'

4. **Check database exists**

   .. code-block:: sql

       SHOW DATABASES LIKE 'medilink';

Table Not Found
---------------

**Symptom**: "Table 'doctors' doesn't exist" error

**Solution**: Initialize database

.. code-block:: bash

    # Run initialization script
    python database/init_db.py

Or manually create tables:

.. code-block:: sql

    CREATE TABLE doctors (
        doctor_id INT PRIMARY KEY AUTO_INCREMENT,
        full_name VARCHAR(100) NOT NULL,
        specialty VARCHAR(50),
        phone VARCHAR(20) UNIQUE,
        email VARCHAR(100) UNIQUE,
        experience INT,
        license_number VARCHAR(50) UNIQUE,
        password VARCHAR(255),
        is_active TINYINT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

Duplicate Entry Error
---------------------

**Symptom**: "Duplicate entry '...' for key '...'"

**Solutions**:

1. **Identify constraint** from error message
2. **Find existing record**

   .. code-block:: sql

       SELECT * FROM doctors WHERE email='duplicate@email.com';

3. **Delete or modify** existing record
4. **Retry operation**

Application Issues
==================

Blank Page Error
----------------

**Symptom**: Completely blank page when accessing admin panel

**Possible Causes**:

1. Python error/crash
2. Template file missing
3. Syntax error in code

**Solutions**:

1. **Check console output**
   - Look for Python error messages
   - Python traceback will appear

2. **Verify templates exist**

   .. code-block:: bash

       ls templates/admin/
       # Should see: dashboard.html, doctors.html, etc.

3. **Check Flask debug mode**

   .. code-block:: python

       app.run(debug=True)  # Enable for detailed errors

500 Internal Server Error
--------------------------

**Symptom**: "Internal Server Error" page

**Possible Causes**:

1. Python exception
2. Unhandled error
3. Missing import

**Solutions**:

1. **Enable debug mode** in app.py

   .. code-block:: python

       app.run(debug=True)

2. **Check error logs** in terminal output

3. **Review recent code changes**

Permission Denied
-----------------

**Symptom**: "Permission denied" or "Access forbidden"

**Solutions**:

1. **Verify you're admin**
   - Login with admin account
   - Check session user_type = 'admin'

2. **Check route permissions**
   - Route should verify: ``session.get('user_type') != 'admin'``

3. **Clear cache**
   - Ctrl+F5 (hard refresh)
   - Clear browser cache

Performance Issues
==================

High Server CPU/Memory
----------------------

**Symptom**: Server running slow, high resource usage

**Solutions**:

1. **Check running processes**

   .. code-block:: bash

       ps aux | grep python
       ps aux | grep mysql

2. **Monitor with Activity Monitor** or Task Manager

3. **Restart application**

   .. code-block:: bash

       # Kill Flask app
       Ctrl+C in terminal
       
       # Restart
       python app.py

4. **Check for infinite loops**
   - Review recent code changes
   - Check database queries

Timeout Errors
--------------

**Symptom**: "Connection timed out" or operation takes very long

**Solutions**:

1. **Increase timeout**

   .. code-block:: python

       app.config['MYSQL_CONNECT_TIMEOUT'] = 30

2. **Optimize queries**
   - Add database indexes
   - Use LIMIT for pagination

3. **Check network** connection

Debugging Tips
==============

Enable Debug Logging
---------------------

In app.py:

.. code-block:: python

    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

Print Debug Information
------------------------

.. code-block:: python

    @app.route('/admin/doctors')
    def admin_doctors():
        print(f"User: {session.get('username')}")
        print(f"Type: {session.get('user_type')}")
        # ... rest of code

Check Request Data
-------------------

.. code-block:: python

    print(f"Method: {request.method}")
    print(f"Form data: {request.form}")
    print(f"Args: {request.args}")

Database Query Debugging
------------------------

.. code-block:: python

    cursor.execute("SELECT * FROM doctors LIMIT 1")
    result = cursor.fetchone()
    print(f"Query result: {result}")

Browser Console Errors
-----------------------

In Firefox/Chrome:
- Right-click → Inspect → Console tab
- Look for JavaScript errors
- Check Network tab for failed requests

Getting Help
============

If Issue Persists:

1. **Check logs** (terminal output, MySQL logs)
2. **Review documentation** for similar issues
3. **Verify setup** against installation guide
4. **Test database** connection separately
5. **Review code** for recent changes
6. **Search documentation** for solution
7. **Contact support** with error details

Essential Debug Information to Provide:

- Error message (exact text)
- Operation attempted
- Browser console errors
- Terminal/application logs
- Database connection details (sanitized)
- Python/Flask versions
- MySQL version

Next Steps
==========

1. **Re-read Admin Guide** → See :doc:`overview`
2. **Check API Reference** → See :doc:`api_endpoints`
3. **Review Examples** → See :doc:`examples`
4. **System Architecture** → See :doc:`overview`
