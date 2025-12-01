"""
Doctor Model - Al Mamun Oualid
"""

from werkzeug.security import generate_password_hash, check_password_hash


class Doctor:
    
    @staticmethod
    def create(mysql, doctor_code, password, full_name, university, email, phone, 
               specialization=None, qualification=None, address=None, created_by=None):
        cursor = mysql.connection.cursor()
        hashed_password = generate_password_hash(password)
        
        # Insert into database
        cursor.execute("""
            INSERT INTO doctors (doctor_code, password, full_name, university, specialization,
                               qualification, email, phone, address, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (doctor_code, hashed_password, full_name, university, specialization,
              qualification, email, phone, address, created_by))
        
        mysql.connection.commit()
        doctor_id = cursor.lastrowid
        cursor.close()
        
        return doctor_id
    
    @staticmethod
    def find_by_code(mysql, doctor_code):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM doctors WHERE doctor_code = %s AND is_active = TRUE", 
            (doctor_code,)
        )
        doctor = cursor.fetchone()
        cursor.close()
        
        return doctor
    
    @staticmethod
    def find_by_id(mysql, doctor_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
        doctor = cursor.fetchone()
        cursor.close()
        
        return doctor
    
    @staticmethod
    def get_all(mysql, active_only=True):
        cursor = mysql.connection.cursor()
        
        if active_only:
            cursor.execute(
                "SELECT * FROM doctors WHERE is_active = TRUE ORDER BY full_name"
            )
        else:
            cursor.execute("SELECT * FROM doctors ORDER BY full_name")
        
        doctors = cursor.fetchall()
        cursor.close()
        
        return doctors
    
    @staticmethod
    def verify_password(mysql, doctor_code, password):
        doctor = Doctor.find_by_code(mysql, doctor_code)
        if doctor and check_password_hash(doctor['password'], password):
            return doctor
        return None
    
    @staticmethod
    def update(mysql, doctor_id, **kwargs):
        cursor = mysql.connection.cursor()
        fields = []
        values = []
        
        for key, value in kwargs.items():
            if key == 'password':
                value = generate_password_hash(value)
            fields.append(f"{key} = %s")
            values.append(value)
        
        values.append(doctor_id)
        query = f"UPDATE doctors SET {', '.join(fields)} WHERE doctor_id = %s"
        cursor.execute(query, values)
        
        mysql.connection.commit()
        cursor.close()
        
        return True
    
    @staticmethod
    def delete(mysql, doctor_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE doctors SET is_active = FALSE WHERE doctor_id = %s", 
            (doctor_id,)
        )
        mysql.connection.commit()
        cursor.close()
        
        return True
    
    @staticmethod
    def get_by_university(mysql, university):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT * FROM doctors 
            WHERE university = %s AND is_active = TRUE 
            ORDER BY full_name
        """, (university,))
        doctors = cursor.fetchall()
        cursor.close()
        
        return doctors
