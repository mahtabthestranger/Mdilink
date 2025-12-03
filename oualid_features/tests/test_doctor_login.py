"""
Unit Tests for F3: Doctor Login
Al Mamun Oualid
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from oualid_features.models.doctor_model import Doctor


class TestDoctorLogin(unittest.TestCase):
    
    def setUp(self):
        self.mock_mysql = Mock()
        self.mock_cursor = MagicMock()
        self.mock_mysql.connection.cursor.return_value = self.mock_cursor
    
    def test_verify_password_valid_credentials(self):
        """Test F3: Valid doctor login credentials"""
        self.mock_cursor.fetchone.return_value = {
            'doctor_id': 1,
            'doctor_code': 'DOC001',
            'full_name': 'Dr. John Smith',
            'password': 'pbkdf2:sha256:600000$xyz$abc123',
            'is_active': True
        }
        
        with patch('oualid_features.models.doctor_model.check_password_hash', return_value=True):
            result = Doctor.verify_password(self.mock_mysql, 'DOC001', 'password123')
            
            self.assertIsNotNone(result)
            self.assertEqual(result['doctor_code'], 'DOC001')
            self.assertEqual(result['full_name'], 'Dr. John Smith')
    
    def test_verify_password_invalid_credentials(self):
        """Test F3: Invalid doctor login credentials"""
        self.mock_cursor.fetchone.return_value = {
            'doctor_id': 1,
            'doctor_code': 'DOC001',
            'password': 'pbkdf2:sha256:600000$xyz$abc123'
        }
        
        with patch('oualid_features.models.doctor_model.check_password_hash', return_value=False):
            result = Doctor.verify_password(self.mock_mysql, 'DOC001', 'wrongpassword')
            
            self.assertIsNone(result)
    
    def test_verify_password_nonexistent_doctor(self):
        """Test F3: Login with non-existent doctor code"""
        self.mock_cursor.fetchone.return_value = None
        
        result = Doctor.verify_password(self.mock_mysql, 'INVALID', 'password123')
        
        self.assertIsNone(result)
    
    def test_find_by_code_active_doctor(self):
        """Test finding active doctor by code"""
        self.mock_cursor.fetchone.return_value = {
            'doctor_id': 1,
            'doctor_code': 'DOC001',
            'full_name': 'Dr. John Smith',
            'is_active': True
        }
        
        result = Doctor.find_by_code(self.mock_mysql, 'DOC001')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['doctor_code'], 'DOC001')
        self.mock_cursor.execute.assert_called_once()
    
    def test_password_hashing(self):
        """Test F3: Password is properly hashed"""
        with patch('oualid_features.models.doctor_model.generate_password_hash', return_value='hashed_password'):
            Doctor.create(
                self.mock_mysql,
                doctor_code='DOC002',
                password='plaintext',
                full_name='Dr. Jane Doe',
                university='Medical University',
                email='jane@example.com',
                phone='1234567890'
            )
            
            call_args = self.mock_cursor.execute.call_args[0]
            self.assertIn('hashed_password', call_args[1])


if __name__ == '__main__':
    unittest.main()
