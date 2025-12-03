View Appointments (F4)
======================

Overview
--------
The View Appointments feature allows doctors to manage their daily schedule. It provides a comprehensive view of all patient appointments with filtering capabilities.

Features
--------
*   **List View**: Displays all appointments sorted by date and time.
*   **Filtering**:
    *   **By Date**: View appointments for a specific day.
    *   **By Status**: Filter by Scheduled, Completed, or Cancelled status.
*   **Status Updates**: Mark appointments as Completed or Cancelled directly from the list.
*   **Patient Details**: Quick access to patient information for each appointment.

Implementation Details
----------------------
This feature is implemented in the ``doctor_appointments`` route. It utilizes the ``Appointment`` model to fetch data with complex joins for patient details.

**Key Components:**

1.  **Route**: ``/doctor/appointments``
2.  **Template**: ``templates/doctor/appointments.html``
3.  **Model Method**: ``Appointment.get_by_doctor()``

Usage
-----
1.  Log in to the doctor dashboard.
2.  Click on "Appointments" in the navigation.
3.  Use the date picker to select a specific date.
4.  Use the status dropdown to filter by appointment status.
5.  Click "Update" on an appointment card to change its status.
