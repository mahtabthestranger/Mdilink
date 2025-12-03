"""
Appointment Model
Handles all database operations related to appointments
"""

class Appointment:
    """Appointment model class"""
    
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
        """Find appointment by ID"""
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
        """Get all appointments for a doctor with optional filters"""
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
        """Update appointment status"""
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
