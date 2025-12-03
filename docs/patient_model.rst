Patient Model
=============

Developer: Mahtab Ahmed

File: ``models/patient.py``

Description
-----------
This module handles all database operations related to patients including registration, login verification, and session management.

Class: Patient
--------------

.. py:class:: Patient

   Patient model class for database operations.

Methods
-------

.. py:method:: Patient.create(mysql, full_name, age, gender, phone, email, password, address=None, blood_group=None, emergency_contact=None)

   Create a new patient account in the database.

   :param mysql: MySQL database connection object
   :param full_name: Patient's full name
   :param age: Patient's age
   :param gender: Patient's gender (Male/Female/Other)
   :param phone: Patient's phone number
   :param email: Patient's email address (unique)
   :param password: Plain text password (will be hashed)
   :param address: Patient's address (optional)
   :param blood_group: Patient's blood group (optional)
   :param emergency_contact: Emergency contact number (optional)
   :return: The newly created patient's ID

.. py:method:: Patient.find_by_email(mysql, email)

   Find a patient by their email address.

   :param mysql: MySQL database connection object
   :param email: Email address to search for
   :return: Patient record if found, None otherwise

.. py:method:: Patient.find_by_id(mysql, patient_id)

   Find a patient by their ID.

   :param mysql: MySQL database connection object
   :param patient_id: Patient's unique ID
   :return: Patient record if found, None otherwise

.. py:method:: Patient.get_all(mysql)

   Get all active patients from the database.

   :param mysql: MySQL database connection object
   :return: List of all active patient records

.. py:method:: Patient.verify_password(mysql, email, password)

   Verify patient login credentials.

   :param mysql: MySQL database connection object
   :param email: Patient's email address
   :param password: Plain text password to verify
   :return: Patient record if credentials valid, None otherwise

.. py:method:: Patient.update(mysql, patient_id, **kwargs)

   Update patient details in the database.

   :param mysql: MySQL database connection object
   :param patient_id: Patient's unique ID
   :param kwargs: Fields to update (key=value pairs)
   :return: True if update successful

.. py:method:: Patient.email_exists(mysql, email)

   Check if an email address is already registered.

   :param mysql: MySQL database connection object
   :param email: Email address to check
   :return: True if email exists, False otherwise

.. py:method:: Patient.delete(mysql, patient_id)

   Soft delete a patient (set is_active to False).

   :param mysql: MySQL database connection object
   :param patient_id: Patient's unique ID
   :return: True if deletion successful

