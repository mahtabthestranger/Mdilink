"""
Unit Tests for Password Reset Feature
"""

import unittest
from tests.test_base import BaseTestCase
from models.patient import Patient
from models.password_reset import PasswordReset
from flask_mysqldb import MySQL

class TestPasswordReset(BaseTestCase):
    """Test password reset features"""
    
    def setUp(self):
        """Set up test data"""
        super().setUp()
        
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            # Create test patient
            self.patient_id = Patient.create(
                mysql, 'Test Patient', 30, 'Male', '1234567890',
                'patient@test.com', 'password123'
            )
    
    def test_create_reset_token(self):
        """Test creating a password reset token"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            token = PasswordReset.create_token(
                mysql, 'patient', self.patient_id, 'patient@test.com'
            )
            
            self.assertIsNotNone(token)
            self.assertGreater(len(token), 20)
    
    def test_verify_valid_token(self):
        """Test verifying a valid token"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            # Create token
            token = PasswordReset.create_token(
                mysql, 'patient', self.patient_id, 'patient@test.com'
            )
            
            # Verify token
            token_data = PasswordReset.verify_token(mysql, token)
            
            self.assertIsNotNone(token_data)
            self.assertEqual(token_data['user_type'], 'patient')
            self.assertEqual(token_data['user_id'], self.patient_id)
    
    def test_verify_invalid_token(self):
        """Test verifying an invalid token"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            token_data = PasswordReset.verify_token(mysql, 'invalid_token')
            
            self.assertIsNone(token_data)
    
    def test_delete_token(self):
        """Test deleting a token"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            # Create token
            token = PasswordReset.create_token(
                mysql, 'patient', self.patient_id, 'patient@test.com'
            )
            
            # Delete token
            result = PasswordReset.delete_token(mysql, token)
            self.assertTrue(result)
            
            # Verify it's deleted
            token_data = PasswordReset.verify_token(mysql, token)
            self.assertIsNone(token_data)
    
    def test_find_user_by_email(self):
        """Test finding user by email"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            user = PasswordReset.find_user_by_email(
                mysql, 'patient@test.com', 'patient'
            )
            
            self.assertIsNotNone(user)
            self.assertEqual(user['email'], 'patient@test.com')

if __name__ == '__main__':
    unittest.main()
