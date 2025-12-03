Doctor Login (F3)
=================

Overview
--------
The Doctor Login feature serves as the secure entry point for medical professionals to access the Medilink system. It ensures that only authorized doctors can view patient data and manage appointments.

Features
--------
*   **Secure Authentication**: Verifies doctor credentials against the database.
*   **Session Management**: Maintains user state securely during the session.
*   **Access Control**: Restricts access to authorized doctor pages only.
*   **Account Validation**: Checks if the doctor's account is active before allowing login.

Implementation Details
----------------------
The login process is handled by the ``doctor_login`` route in ``app.py``. It uses the ``Doctor`` model to verify the password hash.

**Key Components:**

1.  **Route**: ``/doctor/login`` (GET/POST)
2.  **Template**: ``templates/doctor/login.html``
3.  **Model Method**: ``Doctor.verify_password()``

Usage
-----
1.  Navigate to the doctor login page.
2.  Enter your Doctor ID (e.g., DOC001).
3.  Enter your password.
4.  Click "Login".
5.  Upon success, you will be redirected to the dashboard.
