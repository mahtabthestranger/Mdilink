Mahtabapp - Main Application
============================

**Developer:** Mahtab Ahmed

**File:** ``Mahtabapp.py``

This is the main Flask application that handles all patient authentication routes.

Overview
--------

The Mahtabapp module provides the following features:

* Patient Registration
* Patient Login with Session Management
* Patient Dashboard (Protected Route)
* Logout Functionality

Routes
------

index()
^^^^^^^

.. py:function:: index()

   Redirect to patient login page.

   :route: ``/``
   :methods: GET
   :returns: Redirect to ``/patient/login``

patient_register()
^^^^^^^^^^^^^^^^^^

.. py:function:: patient_register()

   Handle patient registration with form validation.

   :route: ``/patient/register``
   :methods: GET, POST
   :returns: Registration form (GET) or redirect after registration (POST)

   **Validation:**

   * All required fields must be filled
   * Password must match confirmation
   * Password must be at least 6 characters
   * Email must not already exist

   **Form Fields:**

   * ``full_name`` - Patient's full name (required)
   * ``age`` - Patient's age (required)
   * ``gender`` - Patient's gender (required)
   * ``phone`` - Phone number (required)
   * ``email`` - Email address (required)
   * ``password`` - Password (required)
   * ``confirm_password`` - Password confirmation (required)
   * ``address`` - Address (optional)
   * ``blood_group`` - Blood group (optional)
   * ``emergency_contact`` - Emergency contact (optional)

patient_login()
^^^^^^^^^^^^^^^

.. py:function:: patient_login()

   Handle patient login with session management.

   :route: ``/patient/login``
   :methods: GET, POST
   :returns: Login form (GET) or redirect to dashboard (POST)

   **Session Variables Set:**

   * ``user_type`` - Set to 'patient'
   * ``user_id`` - Patient ID from database
   * ``user_name`` - Patient's full name
   * ``user_email`` - Patient's email

patient_dashboard()
^^^^^^^^^^^^^^^^^^^

.. py:function:: patient_dashboard()

   Display patient dashboard (protected route).

   :route: ``/patient/dashboard``
   :methods: GET
   :returns: Dashboard template or redirect to login if not authenticated

logout()
^^^^^^^^

.. py:function:: logout()

   Clear session and logout user.

   :route: ``/logout``
   :methods: GET
   :returns: Redirect to login page

forgot_password()
^^^^^^^^^^^^^^^^^

.. py:function:: forgot_password()

   Placeholder for forgot password functionality.

   :route: ``/forgot-password``
   :methods: GET
   :returns: Redirect to login page

patient_book_appointment()
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: patient_book_appointment()

   Placeholder for book appointment functionality.

   :route: ``/patient/book-appointment``
   :methods: GET
   :returns: Redirect to dashboard or login

patient_appointments()
^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: patient_appointments()

   Placeholder for view appointments functionality.

   :route: ``/patient/appointments``
   :methods: GET
   :returns: Redirect to dashboard or login

patient_medical_records()
^^^^^^^^^^^^^^^^^^^^^^^^^

.. py:function:: patient_medical_records()

   Placeholder for medical records functionality.

   :route: ``/patient/medical-records``
   :methods: GET
   :returns: Redirect to dashboard or login

