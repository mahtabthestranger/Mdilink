"""
Patient Model
Handles all database operations related to patients
"""

from werkzeug.security import generate_password_hash, check_password_hash

class Patient:
    """Patient model class"""
    
    @staticmethod
    def create(mysql, full_name, age, gender, phone, email, password, 
               address=None, blood_group=None, emergency_contact=None):
        """Create a new patient"""
        cursor = mysql.connection.cursor()
        hashed_password = generate_password_hash(password)
        
        cursor.execute("""
            INSERT INTO patients (full_name, age, gender, phone, email, password,
                                address, blood_group, emergency_contact)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (full_name, age, gender, phone, email, hashed_password,
              address, blood_group, emergency_contact))
        
        mysql.connection.commit()
        patient_id = cursor.lastrowid
        cursor.close()
        return patient_id
    
    @staticmethod
    def find_by_email(mysql, email):
        """Find patient by email"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM patients WHERE email = %s AND is_active = TRUE", (email,))
        patient = cursor.fetchone()
        cursor.close()
        return patient
    
    @staticmethod
    def find_by_id(mysql, patient_id):
        """Find patient by ID"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
        patient = cursor.fetchone()
        cursor.close()
        return patient
    
    @staticmethod
    def get_all(mysql):
        """Get all patients"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM patients WHERE is_active = TRUE ORDER BY full_name")
        patients = cursor.fetchall()
        cursor.close()
        return patients
    
    @staticmethod
    def verify_password(mysql, email, password):
        """Verify patient password"""
        patient = Patient.find_by_email(mysql, email)
        if patient and check_password_hash(patient['password'], password):
            return patient
        return None
    
    @staticmethod
    def update(mysql, patient_id, **kwargs):
        """Update patient details"""
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
        """Check if email already exists"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT patient_id FROM patients WHERE email = %s", (email,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def delete(mysql, patient_id):
        """Delete (soft delete) patient"""
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE patients SET is_active = FALSE WHERE patient_id = %s", (patient_id,))
        mysql.connection.commit()
        cursor.close()
        return True
