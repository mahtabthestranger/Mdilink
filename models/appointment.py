"""
Appointment Model
=================

Handles all database operations related to appointments including scheduling,
retrieval, and status management.

Author: Multiple team members
Feature F4 (View Appointments): Al Mamun Oualid
"""

class Appointment:
    """
    Appointment model class for managing patient-doctor appointments.
    
    This class provides static methods for creating, retrieving, and managing
    appointments in the hospital management system.
    
    Attributes:
        None (all methods are static)
    """
    
    @staticmethod
    def create(mysql, patient_id, doctor_id, appointment_date, appointment_time, reason=None):
        """Create a new appointment"""
        cursor = mysql.connection.cursor()
        
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, appointment_date, 
                                    appointment_time, reason, status)
            VALUES (%s, %s, %s, %s, %s, 'Scheduled')
        """, (patient_id, doctor_id, appointment_date, appointment_time, reason))
        
        mysql.connection.commit()
        appointment_id = cursor.lastrowid
        cursor.close()
        return appointment_id
    
    @staticmethod
    def find_by_id(mysql, appointment_id):
        """
        Find an appointment by its ID with patient and doctor information.
        
        Args:
            mysql: MySQL database connection object
            appointment_id (int): ID of the appointment
        
        Returns:
            dict: Appointment record with patient and doctor details, None if not found
        
        Example:
            >>> appointment = Appointment.find_by_id(mysql, 1)
            >>> if appointment:
            ...     print(f"Patient: {appointment['patient_name']}")
            ...     print(f"Doctor: {appointment['doctor_name']}")
        
        Note:
            Used in F4 to verify appointment ownership before status updates
        """
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT a.*, p.full_name as patient_name, d.full_name as doctor_name,
                   d.university, d.specialization
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.appointment_id = %s
        """, (appointment_id,))
        appointment = cursor.fetchone()
        cursor.close()
        return appointment
    
    @staticmethod
    def get_by_patient(mysql, patient_id):
        """Get all appointments for a patient"""
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT a.*, d.full_name as doctor_name, d.university, d.specialization
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE a.patient_id = %s
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """, (patient_id,))
        appointments = cursor.fetchall()
        cursor.close()
        return appointments
    
    @staticmethod
    def get_by_doctor(mysql, doctor_id, date_filter=None, status_filter=None):
        """
        Get all appointments for a doctor with optional filters (F4: View Appointments).
        
        This method is the core of F4 feature, allowing doctors to view their
        appointments with filtering capabilities.
        
        Args:
            mysql: MySQL database connection object
            doctor_id (int): ID of the doctor
            date_filter (str, optional): Filter by date (YYYY-MM-DD format). Defaults to None.
            status_filter (str, optional): Filter by status (Scheduled/Completed/Cancelled).
                                          Defaults to None.
        
        Returns:
            list: List of appointments with patient information, ordered by date (newest first)
        
        Example:
            >>> # Get all appointments
            >>> appointments = Appointment.get_by_doctor(mysql, doctor_id=1)
            >>> 
            >>> # Filter by date
            >>> today_appointments = Appointment.get_by_doctor(
            ...     mysql, doctor_id=1, date_filter='2025-12-01'
            ... )
            >>> 
            >>> # Filter by status
            >>> scheduled = Appointment.get_by_doctor(
            ...     mysql, doctor_id=1, status_filter='Scheduled'
            ... )
        
        Note:
            - Results include patient details through JOIN query
            - Filters can be combined (date AND status)
            - Used in F4: View Appointments feature
        """
        cursor = mysql.connection.cursor()
        
        query = """
            SELECT a.*, p.full_name as patient_name, p.age, p.gender, p.phone
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = %s
        """
        params = [doctor_id]
        
        if date_filter:
            query += " AND a.appointment_date = %s"
            params.append(date_filter)
            
        if status_filter:
            query += " AND a.status = %s"
            params.append(status_filter)
            
        query += " ORDER BY a.appointment_date DESC, a.appointment_time DESC"
        
        cursor.execute(query, tuple(params))
        appointments = cursor.fetchall()
        cursor.close()
        return appointments
    
    @staticmethod
    def check_availability(mysql, doctor_id, appointment_date, appointment_time):
        """Check if a time slot is available"""
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT appointment_id FROM appointments
            WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
            AND status != 'Cancelled'
        """, (doctor_id, appointment_date, appointment_time))
        result = cursor.fetchone()
        cursor.close()
        return result is None
    
    @staticmethod
    def update_status(mysql, appointment_id, status, notes=None):
        """
        Update appointment status (F4: View Appointments).
        
        Allows doctors to mark appointments as Completed or Cancelled.
        
        Args:
            mysql: MySQL database connection object
            appointment_id (int): ID of the appointment to update
            status (str): New status ('Scheduled', 'Completed', or 'Cancelled')
            notes (str, optional): Additional notes about the status change. Defaults to None.
        
        Returns:
            bool: True if update successful
        
        Example:
            >>> # Mark appointment as completed
            >>> Appointment.update_status(mysql, appointment_id=1, status='Completed')
            >>> 
            >>> # Cancel with notes
            >>> Appointment.update_status(
            ...     mysql,
            ...     appointment_id=2,
            ...     status='Cancelled',
            ...     notes='Patient requested cancellation'
            ... )
        
        Note:
            - Only Scheduled appointments should be updated
            - Used in F4: View Appointments feature
            - Access control is enforced in the route layer
        """
        cursor = mysql.connection.cursor()
        
        if notes:
            cursor.execute("""
                UPDATE appointments 
                SET status = %s, notes = %s 
                WHERE appointment_id = %s
            """, (status, notes, appointment_id))
        else:
            cursor.execute("""
                UPDATE appointments 
                SET status = %s 
                WHERE appointment_id = %s
            """, (status, appointment_id))
        
        mysql.connection.commit()
        cursor.close()
        return True
    
    @staticmethod
    def get_upcoming_by_doctor(mysql, doctor_id):
        """Get upcoming appointments for a doctor"""
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT a.*, p.full_name as patient_name, p.age, p.gender, p.phone
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = %s 
            AND a.appointment_date >= CURDATE()
            AND a.status = 'Scheduled'
            ORDER BY a.appointment_date, a.appointment_time
        """, (doctor_id,))
        appointments = cursor.fetchall()
        cursor.close()
        return appointments
    
    @staticmethod
    def get_all(mysql):
        """Get all appointments (for admin)"""
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT a.*, 
                   p.full_name as patient_name, p.phone as patient_phone,
                   d.full_name as doctor_name, d.university
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """, ())
        appointments = cursor.fetchall()
        cursor.close()
        return appointments
