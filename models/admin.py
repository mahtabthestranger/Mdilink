"""
Admin Model
Handles all database operations related to administrators
"""

from werkzeug.security import generate_password_hash, check_password_hash

class Admin:
    """Admin model class"""
    
    @staticmethod
    def create(mysql, username, password, full_name, email, phone=None):
        """Create a new admin"""
        cursor = mysql.connection.cursor()
        hashed_password = generate_password_hash(password)
        
        cursor.execute("""
            INSERT INTO admins (username, password, full_name, email, phone)
            VALUES (%s, %s, %s, %s, %s)
        """, (username, hashed_password, full_name, email, phone))
        
        mysql.connection.commit()
        admin_id = cursor.lastrowid
        cursor.close()
        return admin_id
    
    @staticmethod
    def find_by_username(mysql, username):
        """Find admin by username"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM admins WHERE username = %s AND is_active = TRUE", (username,))
        admin = cursor.fetchone()
        cursor.close()
        return admin
    
    @staticmethod
    def find_by_id(mysql, admin_id):
        """Find admin by ID"""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (admin_id,))
        admin = cursor.fetchone()
        cursor.close()
        return admin
    
    @staticmethod
    def verify_password(mysql, username, password):
        """Verify admin password"""
        admin = Admin.find_by_username(mysql, username)
        if admin and check_password_hash(admin['password'], password):
            return admin
        return None
    
    @staticmethod
    def update(mysql, admin_id, **kwargs):
        """Update admin details"""
        cursor = mysql.connection.cursor()
        
        # Build dynamic update query
        fields = []
        values = []
        for key, value in kwargs.items():
            if key == 'password':
                value = generate_password_hash(value)
            fields.append(f"{key} = %s")
            values.append(value)
        
        values.append(admin_id)
        query = f"UPDATE admins SET {', '.join(fields)} WHERE admin_id = %s"
        
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return True
