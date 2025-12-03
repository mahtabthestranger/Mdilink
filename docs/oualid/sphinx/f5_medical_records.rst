Medical Records (F5)
====================

Overview
--------
The Medical Records Management feature enables doctors to view patient history and add new medical records. This is critical for maintaining continuity of care.

Features
--------
*   **Patient History**: View complete medical history for any patient.
*   **Add Record**: Create new medical records with diagnosis, prescription, and notes.
*   **Edit Record**: Modify existing records (only by the creating doctor).
*   **Patient List**: Browse all patients to access their records.

Implementation Details
----------------------
This feature spans multiple routes for listing patients, viewing details, and managing records. It uses the ``MedicalRecord`` model for data persistence.

**Key Components:**

1.  **Routes**:
    *   ``/doctor/patients``: List all patients
    *   ``/doctor/patient/<id>``: View patient details
    *   ``/doctor/patient/<id>/add-record``: Add new record
2.  **Model Method**: ``MedicalRecord.create()``, ``MedicalRecord.get_by_patient()``

Usage
-----
**Adding a Record:**

1.  Go to "Patients" list.
2.  Select a patient to view their profile.
3.  Click "Add Medical Record".
4.  Fill in the diagnosis, symptoms, and prescription.
5.  Click "Save Record".

**Viewing History:**

1.  Navigate to a patient's profile.
2.  Scroll down to the "Medical History" section.
3.  View past records sorted by date.
