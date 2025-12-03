Database Initialization
=======================

Developer: Mahtab Ahmed

File: ``database/reference_init_db.py``

Description
-----------
This script initializes the Medilink database, creates all necessary tables, and seeds initial admin data.

Functions
---------

.. py:function:: create_database()

   Create the database if it doesn't exist.

   :return: True if successful, False otherwise

.. py:function:: create_tables()

   Create all necessary database tables.

   Tables created:
      - admins
      - doctors
      - patients
      - appointments
      - medical_records
      - password_reset_tokens
      - chat_messages

   :return: True if successful, False otherwise

.. py:function:: seed_admin_data()

   Insert default admin account into the database.

   Default credentials:
      - Username: admin
      - Password: admin123

   :return: True if successful, False otherwise

.. py:function:: main()

   Main initialization function.

   Executes database setup in three steps:
      1. Create database
      2. Create tables
      3. Seed initial data

Database Tables
---------------

patients
^^^^^^^^
Stores patient information:

* patient_id (INT, PRIMARY KEY)
* full_name (VARCHAR)
* age (INT)
* gender (ENUM: Male/Female/Other)
* phone (VARCHAR)
* email (VARCHAR, UNIQUE)
* password (VARCHAR, hashed)
* address (TEXT)
* blood_group (VARCHAR)
* emergency_contact (VARCHAR)
* created_at (TIMESTAMP)
* updated_at (TIMESTAMP)
* is_active (BOOLEAN)

admins
^^^^^^
Stores admin information:

* admin_id (INT, PRIMARY KEY)
* username (VARCHAR, UNIQUE)
* password (VARCHAR, hashed)
* full_name (VARCHAR)
* email (VARCHAR, UNIQUE)
* phone (VARCHAR)
* is_active (BOOLEAN)

doctors
^^^^^^^
Stores doctor information:

* doctor_id (INT, PRIMARY KEY)
* doctor_code (VARCHAR, UNIQUE)
* password (VARCHAR, hashed)
* full_name (VARCHAR)
* university (VARCHAR)
* specialization (VARCHAR)
* qualification (VARCHAR)
* email (VARCHAR, UNIQUE)
* phone (VARCHAR)
* is_active (BOOLEAN)

appointments
^^^^^^^^^^^^
Stores appointment information:

* appointment_id (INT, PRIMARY KEY)
* patient_id (INT, FOREIGN KEY)
* doctor_id (INT, FOREIGN KEY)
* appointment_date (DATE)
* appointment_time (TIME)
* status (ENUM: Scheduled/Completed/Cancelled/No-Show)

Usage
-----
Run the script directly::

   python database/reference_init_db.py

