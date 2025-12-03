"""
Patient Model - Medilink Hospital Management System.

Developer: Mahtab Ahmed
Feature: Patient Authentication, Registration & Login

This module handles all database operations related to patients including:
    - Patient registration with password hashing
    - Patient login verification
    - Session management
"""

from werkzeug.security import generate_password_hash, check_password_hash


class Patient:
    """
    Patient model class for database operations.

    This class provides static methods for patient CRUD operations
    including registration, authentication, and profile management.
    """

    @staticmethod
    def create(mysql, full_name, age, gender, phone, email, password,
               address=None, blood_group=None, emergency_contact=None):
        """
        Create a new patient account in the database.

        Args:
            mysql: MySQL database connection object
            full_name: Patient's full name
            age: Patient's age
            gender: Patient's gender (Male/Female/Other)
            phone: Patient's phone number
            email: Patient's email address (unique)
            password: Plain text password (will be hashed)
            address: Patient's address (optional)
            blood_group: Patient's blood group (optional)
            emergency_contact: Emergency contact number (optional)

        Returns:
            int: The newly created patient's ID
        """
        cursor = mysql.connection.cursor()
        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO patients (full_name, age, gender, phone, email,
                                  password, address, blood_group,
                                  emergency_contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (full_name, age, gender, phone, email, hashed_password,
              address, blood_group, emergency_contact))

        mysql.connection.commit()
        patient_id = cursor.lastrowid
        cursor.close()
        return patient_id

    @staticmethod
    def find_by_email(mysql, email):
        """
        Find a patient by their email address.

        Args:
            mysql: MySQL database connection object
            email: Email address to search for

        Returns:
            dict: Patient record if found, None otherwise
        """
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM patients WHERE email = %s AND is_active = TRUE"
        cursor.execute(query, (email,))
        patient = cursor.fetchone()
        cursor.close()
        return patient

    @staticmethod
    def find_by_id(mysql, patient_id):
        """
        Find a patient by their ID.

        Args:
            mysql: MySQL database connection object
            patient_id: Patient's unique ID

        Returns:
            dict: Patient record if found, None otherwise
        """
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = %s",
                       (patient_id,))
        patient = cursor.fetchone()
        cursor.close()
        return patient

    @staticmethod
    def get_all(mysql):
        """
        Get all active patients from the database.

        Args:
            mysql: MySQL database connection object

        Returns:
            list: List of all active patient records
        """
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM patients WHERE is_active = TRUE ORDER BY full_name"
        cursor.execute(query)
        patients = cursor.fetchall()
        cursor.close()
        return patients

    @staticmethod
    def verify_password(mysql, email, password):
        """
        Verify patient login credentials.

        Args:
            mysql: MySQL database connection object
            email: Patient's email address
            password: Plain text password to verify

        Returns:
            dict: Patient record if credentials valid, None otherwise
        """
        patient = Patient.find_by_email(mysql, email)
        if patient and check_password_hash(patient['password'], password):
            return patient
        return None

    @staticmethod
    def update(mysql, patient_id, **kwargs):
        """
        Update patient details in the database.

        Args:
            mysql: MySQL database connection object
            patient_id: Patient's unique ID
            **kwargs: Fields to update (key=value pairs)

        Returns:
            bool: True if update successful
        """
        cursor = mysql.connection.cursor()

        fields = []
        values = []
        for key, value in kwargs.items():
            if key == 'password':
                value = generate_password_hash(value)
            fields.append(f"{key} = %s")
            values.append(value)

        values.append(patient_id)
        query = f"UPDATE patients SET {', '.join(fields)} WHERE patient_id = %s"

        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return True

    @staticmethod
    def email_exists(mysql, email):
        """
        Check if an email address is already registered.

        Args:
            mysql: MySQL database connection object
            email: Email address to check

        Returns:
            bool: True if email exists, False otherwise
        """
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT patient_id FROM patients WHERE email = %s",
                       (email,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def delete(mysql, patient_id):
        """
        Soft delete a patient (set is_active to False).

        Args:
            mysql: MySQL database connection object
            patient_id: Patient's unique ID

        Returns:
            bool: True if deletion successful
        """
        cursor = mysql.connection.cursor()
        query = "UPDATE patients SET is_active = FALSE WHERE patient_id = %s"
        cursor.execute(query, (patient_id,))
        mysql.connection.commit()
        cursor.close()
        return True
