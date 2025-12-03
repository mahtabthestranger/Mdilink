"""
Medical Record Model
Handles all database operations related to medical records
"""

class MedicalRecord:
    
    @staticmethod
    def create(mysql, patient_id, doctor_id, visit_date, diagnosis, 
               symptoms=None, prescription=None, tests_recommended=None, 
               follow_up_date=None, notes=None, appointment_id=None):
        """Create a new medical record"""
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
        """Find medical record by ID"""
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
        """Get all medical records for a patient"""
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
        """Get all medical records created by a doctor"""
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
        """Update medical record"""
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
        """Get patient's medical history for a specific doctor"""
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT * FROM medical_records
            WHERE patient_id = %s AND doctor_id = %s
            ORDER BY visit_date DESC
        """, (patient_id, doctor_id))
        records = cursor.fetchall()
        cursor.close()
        return records

