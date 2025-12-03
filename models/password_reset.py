"""
Password Reset Model
Handles password reset token generation and validation
"""

import secrets
from datetime import datetime, timedelta

class PasswordReset:
    """Password reset token model"""
    
    @staticmethod
    def create_token(mysql, user_type, user_id, email):
        """Create a password reset token"""
        cursor = mysql.connection.cursor()
        
        # Generate secure token
        token = secrets.token_urlsafe(32)
        
        # Token expires in 1 hour
        expires_at = datetime.now() + timedelta(hours=1)
        
        # Delete any existing tokens for this user
        cursor.execute("""
            DELETE FROM password_reset_tokens 
            WHERE user_type = %s AND user_id = %s
        """, (user_type, user_id))
        
        # Insert new token
        cursor.execute("""
            INSERT INTO password_reset_tokens 
            (user_type, user_id, email, token, expires_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_type, user_id, email, token, expires_at))
        
        mysql.connection.commit()
        cursor.close()
        
        return token
    
    @staticmethod
    def verify_token(mysql, token):
        """Verify a password reset token"""
        cursor = mysql.connection.cursor()
        
        cursor.execute("""
            SELECT user_type, user_id, email, expires_at
            FROM password_reset_tokens
            WHERE token = %s
        """, (token,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if not result:
            return None
        
        # Check if token has expired
        if result['expires_at'] < datetime.now():
            return None
        
        return result
    
    @staticmethod
    def delete_token(mysql, token):
        """Delete a password reset token after use"""
        cursor = mysql.connection.cursor()
        
        cursor.execute("""
            DELETE FROM password_reset_tokens 
            WHERE token = %s
        """, (token,))
        
        mysql.connection.commit()
        cursor.close()
        
        return True
    
    @staticmethod
    def find_user_by_email(mysql, email, user_type):
        """Find user by email and type"""
        cursor = mysql.connection.cursor()
        
        if user_type == 'patient':
            cursor.execute("""
                SELECT patient_id as user_id, email, full_name
                FROM patients
                WHERE email = %s AND is_active = TRUE
            """, (email,))
        elif user_type == 'doctor':
            cursor.execute("""
                SELECT doctor_id as user_id, email, full_name
                FROM doctors
                WHERE email = %s AND is_active = TRUE
            """, (email,))
        elif user_type == 'admin':
            cursor.execute("""
                SELECT admin_id as user_id, email, full_name
                FROM admins
                WHERE email = %s AND is_active = TRUE
            """, (email,))
        else:
            cursor.close()
            return None
        
        result = cursor.fetchone()
        cursor.close()
        
        return result
