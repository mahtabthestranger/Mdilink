"""
Medical Record Model
====================

Handles all database operations related to patient medical records including
diagnosis, prescriptions, symptoms, and treatment history.

Author: Al Mamun Oualid
Feature: F5 (Medical Records Management)
"""

class MedicalRecord:
    """
    Medical Record model class for managing patient medical records.
    
    This class provides static methods for creating, retrieving, and updating
    medical records created by doctors during patient visits.
    
    Attributes:
        None (all methods are static)
    
    Example:
        >>> record_id = MedicalRecord.create(
        ...     mysql=mysql,
        ...     patient_id=1,
        ...     doctor_id=1,
        ...     visit_date=date.today(),
        ...     diagnosis='Common Cold'
        ... )
    """
    
    @staticmethod
    def create(mysql, patient_id, doctor_id, visit_date, diagnosis, 
               symptoms=None, prescription=None, tests_recommended=None, 
               follow_up_date=None, notes=None, appointment_id=None):
        """
        Create a new medical record for a patient (F5: Medical Records).
        
        Args:
            mysql: MySQL database connection object
            patient_id (int): ID of the patient
            doctor_id (int): ID of the doctor creating the record
            visit_date (date): Date of the visit
            diagnosis (str): Primary diagnosis (required)
            symptoms (str, optional): Patient's symptoms. Defaults to None.
            prescription (str, optional): Prescribed medication. Defaults to None.
            tests_recommended (str, optional): Recommended tests. Defaults to None.
            follow_up_date (date, optional): Follow-up appointment date. Defaults to None.
            notes (str, optional): Additional notes. Defaults to None.
            appointment_id (int, optional): Related appointment ID. Defaults to None.
        
        Returns:
            int: The ID of the newly created medical record
        
        Raises:
            Exception: If database operation fails
        
        Example:
            >>> from datetime import date
            >>> record_id = MedicalRecord.create(
            ...     mysql=mysql,
            ...     patient_id=1,
            ...     doctor_id=1,
            ...     visit_date=date.today(),
            ...     diagnosis='Hypertension',
            ...     symptoms='Headache, dizziness',
            ...     prescription='Lisinopril 10mg daily',
            ...     tests_recommended='Blood pressure monitoring'
            ... )
        
        Note:
            - Diagnosis is a required field
            - Visit date is automatically set to current date in the route
            - Doctor ID comes from the session
        """
        cursor = mysql.connection.cursor()
        
        cursor.execute("""
            INSERT INTO medical_records (patient_id, doctor_id, appointment_id, visit_date,
                                        diagnosis, symptoms, prescription, tests_recommended,
                                        follow_up_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (patient_id, doctor_id, appointment_id, visit_date, diagnosis, symptoms,
              prescription, tests_recommended, follow_up_date, notes))
        
        mysql.connection.commit()
        record_id = cursor.lastrowid
        cursor.close()
        return record_id
    
    @staticmethod
    def find_by_id(mysql, record_id):
        """
        Find a medical record by its ID with patient and doctor information.
        
        Args:
            mysql: MySQL database connection object
            record_id (int): ID of the medical record
        
        Returns:
            dict: Medical record with patient and doctor details, None if not found
        
        Example:
            >>> record = MedicalRecord.find_by_id(mysql, 1)
            >>> if record:
            ...     print(f"Diagnosis: {record['diagnosis']}")
            ...     print(f"Doctor: {record['doctor_name']}")
        """
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT mr.*, 
                   p.full_name as patient_name, p.age, p.gender,
                   d.full_name as doctor_name, d.university, d.specialization
            FROM medical_records mr
            JOIN patients p ON mr.patient_id = p.patient_id
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.record_id = %s
        """, (record_id,))
        record = cursor.fetchone()
        cursor.close()
        return record
    
    @staticmethod
    def get_by_patient(mysql, patient_id):
        """
        Get all medical records for a specific patient (F5: Medical Records).
        
        Args:
            mysql: MySQL database connection object
            patient_id (int): ID of the patient
        
        Returns:
            list: List of medical records ordered by visit date (newest first)
        
        Example:
            >>> records = MedicalRecord.get_by_patient(mysql, patient_id=1)
            >>> for record in records:
            ...     print(f"{record['visit_date']}: {record['diagnosis']}")
            ...     print(f"By Dr. {record['doctor_name']}")
        
        Note:
            Results include doctor information through JOIN
        """
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT mr.*, 
                   d.full_name as doctor_name, d.university, d.specialization
            FROM medical_records mr
            JOIN doctors d ON mr.doctor_id = d.doctor_id
            WHERE mr.patient_id = %s
            ORDER BY mr.visit_date DESC
        """, (patient_id,))
        records = cursor.fetchall()
        cursor.close()
        return records
    
    @staticmethod
    def get_by_doctor(mysql, doctor_id):
        """
        Get all medical records created by a specific doctor.
        
        Args:
            mysql: MySQL database connection object
            doctor_id (int): ID of the doctor
        
        Returns:
            list: List of medical records created by the doctor
        
        Example:
            >>> records = MedicalRecord.get_by_doctor(mysql, doctor_id=1)
            >>> print(f"Total records created: {len(records)}")
        """
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT mr.*, 
                   p.full_name as patient_name, p.age, p.gender
            FROM medical_records mr
            JOIN patients p ON mr.patient_id = p.patient_id
            WHERE mr.doctor_id = %s
            ORDER BY mr.visit_date DESC
        """, (doctor_id,))
        records = cursor.fetchall()
        cursor.close()
        return records
    
    @staticmethod
    def update(mysql, record_id, **kwargs):
        """
        Update an existing medical record (F5: Medical Records).
        
        Args:
            mysql: MySQL database connection object
            record_id (int): ID of the record to update
            **kwargs: Field-value pairs to update
        
        Returns:
            bool: True if update successful
        
        Example:
            >>> MedicalRecord.update(
            ...     mysql,
            ...     record_id=1,
            ...     diagnosis='Updated diagnosis',
            ...     prescription='New medication'
            ... )
        
        Note:
            Only the doctor who created the record should be able to update it
            (enforced in the route layer)
        """
        cursor = mysql.connection.cursor()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = %s")
            values.append(value)
        
        values.append(record_id)
        query = f"UPDATE medical_records SET {', '.join(fields)} WHERE record_id = %s"
        
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return True
    
    @staticmethod
    def get_patient_history(mysql, patient_id, doctor_id):
        """
        Get patient's medical history with a specific doctor.
        
        Args:
            mysql: MySQL database connection object
            patient_id (int): ID of the patient
            doctor_id (int): ID of the doctor
        
        Returns:
            list: List of medical records for this patient-doctor combination
        
        Example:
            >>> history = MedicalRecord.get_patient_history(mysql, patient_id=1, doctor_id=1)
            >>> for record in history:
            ...     print(f"{record['visit_date']}: {record['diagnosis']}")
        """
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT * FROM medical_records
            WHERE patient_id = %s AND doctor_id = %s
            ORDER BY visit_date DESC
        """, (patient_id, doctor_id))
        records = cursor.fetchall()
        cursor.close()
        return records
