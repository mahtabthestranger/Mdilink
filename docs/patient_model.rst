Patient Model
=============

The Patient model handles all database operations for patient authentication.

Location: ``models/patient.py``

Class: Patient
--------------

.. automodule:: models.patient
   :members:
   :undoc-members:
   :show-inheritance:

Methods
-------

create()
^^^^^^^^
Creates a new patient in the database with hashed password.

**Parameters:**

* ``full_name`` - Patient's full name
* ``age`` - Patient's age
* ``gender`` - Male/Female/Other
* ``phone`` - Contact number
* ``email`` - Email address (unique)
* ``password`` - Password (will be hashed)

**Returns:** Patient ID

find_by_email()
^^^^^^^^^^^^^^^
Finds a patient by their email address.

**Parameters:**

* ``email`` - Email to search

**Returns:** Patient record or None

verify_password()
^^^^^^^^^^^^^^^^^
Verifies patient login credentials.

**Parameters:**

* ``email`` - Patient email
* ``password`` - Password to verify

**Returns:** Patient record if valid, None otherwise

email_exists()
^^^^^^^^^^^^^^
Checks if email is already registered.

**Parameters:**

* ``email`` - Email to check

**Returns:** True if exists, False otherwise

