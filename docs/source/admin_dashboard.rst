================================================================================
Admin Dashboard - Statistics & Overview
================================================================================

Dashboard Overview
===================

The admin dashboard provides a comprehensive overview of the Medilink system
with key statistics, metrics, and quick access to management functions.

Admin Dashboard Route
=====================

**Endpoint**: ``/admin/dashboard``

**Methods**: GET

**Description**

Displays the admin dashboard with system statistics, user counts, recent
activity, and quick navigation links.

Request
-------

.. code-block:: bash

    GET /admin/dashboard
    Headers: 
        Cookie: session=<admin_session_id>

Response - Success
------------------

**Status Code**: 200 (OK)

**Content-Type**: text/html

**Rendered Template**: admin/dashboard.html

Response - Unauthorized
------------------------

**Status Code**: 302 (Redirect)

**Location Header**: /admin/login

**Flash Message**: "Please login as admin"

Dashboard Content
=================

Statistics Displayed
--------------------

The dashboard displays the following metrics:

.. list-table::
   :widths: 25 40 35
   :header-rows: 1

   * - Statistic
     - Description
     - Data Source
   * - Total Doctors
     - Count of active doctors
     - SELECT COUNT(*) FROM doctors WHERE is_active = 1
   * - Total Patients
     - Count of active patients
     - SELECT COUNT(*) FROM patients WHERE is_active = 1
   * - Total Appointments
     - Count of all appointments (scheduled/completed)
     - SELECT COUNT(*) FROM appointments
   * - Pending Appointments
     - Count of appointments not yet completed
     - SELECT COUNT(*) FROM appointments WHERE status != 'completed'
   * - Active Users
     - Count of currently logged-in users
     - From session data
   * - System Status
     - Database connection and API health
     - Real-time health check

Statistics Calculation
~~~~~~~~~~~~~~~~~~~~~~

**Total Doctors Query**

.. code-block:: sql

    SELECT COUNT(*) as total
    FROM doctors
    WHERE is_active = 1

**Total Patients Query**

.. code-block:: sql

    SELECT COUNT(*) as total
    FROM patients
    WHERE is_active = 1

**Appointments Query**

.. code-block:: sql

    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) as pending
    FROM appointments

Example Dashboard Display
--------------------------

.. code-block:: text

    ╔════════════════════════════════════════════════════════════╗
    ║              MEDILINK ADMIN DASHBOARD                      ║
    ╠════════════════════════════════════════════════════════════╣
    ║                                                             ║
    ║  Total Doctors: 15          Total Patients: 240            ║
    ║  Total Appointments: 189    Pending: 23                    ║
    ║  System Status: ✓ Healthy   Last Updated: 2024-01-20      ║
    ║                                                             ║
    ╠════════════════════════════════════════════════════════════╣
    ║  QUICK ACTIONS                                             ║
    ║  [Manage Doctors] [Manage Patients] [View Records]         ║
    ║                                                             ║
    ╠════════════════════════════════════════════════════════════╣
    ║  RECENT ACTIVITY                                           ║
    ║  • Doctor added: Dr. Sarah - 2 minutes ago                ║
    ║  • Patient registered: John Doe - 15 minutes ago          ║
    ║  • Appointment scheduled - 1 hour ago                      ║
    ║                                                             ║
    ╚════════════════════════════════════════════════════════════╝

Implementation Details
======================

Dashboard Route Handler
-----------------------

.. code-block:: python

    @app.route('/admin/dashboard')
    def admin_dashboard():
        """
        Display admin dashboard with system statistics.

        Returns:
            Rendered dashboard template with statistics
        
        Raises:
            Redirects to login if not authenticated
        """
       
        if session.get('user_type') != 'admin':
            flash('Please login as admin', 'error')
            return redirect(url_for('admin_login'))

        try:
           
            cursor = mysql.connection.cursor(dictionary=True)

            
            cursor.execute("SELECT COUNT(*) as total FROM doctors WHERE is_active = 1")
            doctors = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM patients WHERE is_active = 1")
            patients = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM appointments")
            appointments = cursor.fetchone()['total']

            cursor.execute("""
                SELECT COUNT(*) as total FROM appointments 
                WHERE status != 'completed'
            """)
            pending = cursor.fetchone()['total']

            cursor.close()

          
            stats = {
                'doctors': doctors,
                'patients': patients,
                'appointments': appointments,
                'pending': pending,
                'admin_name': session.get('user_name', 'Admin'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            return render_template('admin/dashboard.html', stats=stats)

        except Exception as error:
            print(f'Dashboard error: {error}')
            flash('Error loading dashboard', 'error')
            return redirect(url_for('admin_login'))

Data Processing
----------------

The following processing occurs before display:

1. **Aggregation**: Sum counts from multiple tables
2. **Filtering**: Only count active/relevant records
3. **Calculation**: Compute percentages and trends
4. **Formatting**: Convert to display-friendly format
5. **Caching**: Optional caching for performance

Dashboard Components
====================

Statistics Cards
----------------

Each statistic displayed in a card format:

.. code-block:: html

    <div class="stat-card">
        <div class="stat-number">{{ stats.doctors }}</div>
        <div class="stat-label">Active Doctors</div>
        <div class="stat-change">+3 this month</div>
    </div>

Quick Actions Section
---------------------

Provides direct links to management pages:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Action
     - Link Target
   * - Manage Doctors
     - /admin/doctors
   * - Add Doctor
     - /admin/doctors/add
   * - Manage Patients
     - /admin/patients
   * - View Records
     - /admin/patients/medical-records
   * - System Settings
     - /admin/settings
   * - View Logs
     - /admin/logs

Recent Activity Feed
--------------------

Shows recent system events (if implemented):

- Doctor added/modified/deleted
- Patient registered
- Appointments scheduled/completed
- Medical records created
- Password changes
- System events

Each activity shows:
- Event type
- User/entity involved
- Timestamp
- Status (success/failure)

Performance Metrics
===================

Page Load Time
--------------

**Typical Load Time**: 200-500ms

**Factors**:
- Database query complexity
- Number of calculations
- Template rendering time
- Network latency

Database Queries
----------------

**Number of Queries**: 3-4 main queries

**Optimization Tips**:

1. Use indexes on COUNT() queries
2. Cache statistics if accessed frequently
3. Implement pagination for activity feed
4. Use EXPLAIN to analyze query performance

Caching Strategy
----------------

For high-traffic systems, implement caching:

.. code-block:: python

    from flask_caching import Cache

    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    @app.route('/admin/dashboard')
    @cache.cached(timeout=300)  
    def admin_dashboard():
        pass

Responsive Design
=================

The dashboard is responsive across devices:

**Desktop View** (1200px+)
- All statistics displayed in single view
- Four stat cards in row
- Full navigation sidebar

**Tablet View** (768px - 1199px)
- Statistics in 2x2 grid
- Condensed navigation
- Collapsible sections

**Mobile View** (< 768px)
- Statistics stacked vertically
- Hamburger menu navigation
- Single column layout

Example API Response
====================

If dashboard API endpoint exists:

**Request**

.. code-block:: bash

    GET /api/admin/dashboard
    Headers:
        Accept: application/json
        Cookie: session=<session_id>

**Response (JSON)**

.. code-block:: json

    {
        "success": true,
        "data": {
            "statistics": {
                "total_doctors": 15,
                "total_patients": 240,
                "total_appointments": 189,
                "pending_appointments": 23,
                "active_users": 3
            },
            "system_health": {
                "database": "connected",
                "api": "operational",
                "status": "healthy"
            },
            "recent_activity": [
                {
                    "type": "doctor_added",
                    "entity": "Dr. Sarah Johnson",
                    "timestamp": "2024-01-20 14:30:00"
                },
                {
                    "type": "patient_registered",
                    "entity": "John Doe",
                    "timestamp": "2024-01-20 14:15:00"
                }
            ],
            "timestamp": "2024-01-20 14:45:32"
        }
    }

Security Considerations
=======================

Authentication
--------------

- Dashboard requires admin session
- Session verification on each load
- Unauthorized access redirected to login

Authorization
-------------

- Only admins can view dashboard
- Statistics limited to authorized data
- No sensitive patient details exposed

Data Protection
---------------

- Database queries read-only
- No modifications from dashboard view
- User actions logged

Common Tasks
============

View All Doctors
----------------

**From Dashboard**: Click "Manage Doctors" button

**Redirects to**: /admin/doctors (see :doc:`doctor_management`)

View All Patients
-----------------

**From Dashboard**: Click "Manage Patients" button

**Redirects to**: /admin/patients (see :doc:`patient_management`)

Add New Doctor
--------------

**From Dashboard**: Click "Add Doctor" button

**Redirects to**: /admin/doctors/add (see :doc:`doctor_management`)

Troubleshooting
===============

Dashboard Won't Load
--------------------

**Symptom**: Blank dashboard or "Error loading dashboard"

**Solutions**:

1. Verify admin login session
2. Check database connection
3. Review error logs: ``print()`` statements
4. Verify doctor/patient tables exist
5. Check for SQL syntax errors

Statistics Show Zero
--------------------

**Symptom**: All counts show 0

**Solutions**:

1. Verify data exists: ``SELECT COUNT(*) FROM doctors``
2. Check is_active flag: May all be marked inactive
3. Review database queries for WHERE clause issues
4. Ensure MySQL connection is active

Slow Dashboard Load
-------------------

**Symptom**: Dashboard takes 5+ seconds to load

**Solutions**:

1. Add database indexes: ``CREATE INDEX idx_active ON doctors(is_active)``
2. Implement caching for statistics
3. Run EXPLAIN on queries to optimize
4. Check MySQL performance settings
5. Monitor server load during peak times

Next Steps
==========

From the dashboard, you can:

1. **Manage Doctors** → See :doc:`doctor_management`
2. **Manage Patients** → See :doc:`patient_management`
3. **View Records** → See :doc:`api_endpoints`
4. **Reference API** → See :doc:`api_endpoints`
5. **Troubleshoot Issues** → See :doc:`troubleshooting`
