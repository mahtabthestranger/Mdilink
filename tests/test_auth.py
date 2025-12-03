"""
Unit Tests for Authentication (Login/Register)
"""

import unittest
from tests.test_base import BaseTestCase
from models.admin import Admin
from models.doctor import Doctor
from models.patient import Patient
from flask_mysqldb import MySQL

class TestAuthentication(BaseTestCase):
    """Test authentication features"""
    
    def test_admin_login_success(self):
        """Test successful admin login"""
        # Create admin
        with self.app.app_context():
            mysql = MySQL(self.app)
            Admin.create(mysql, 'testadmin', 'password123', 'Test Admin', 
                        'admin@test.com', '1234567890')
        
        # Attempt login
        response = self.client.post('/admin/login', data={
            'username': 'testadmin',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)
    
    def test_admin_login_invalid_credentials(self):
        """Test admin login with invalid credentials"""
        response = self.client.post('/admin/login', data={
            'username': 'invalid',
            'password': 'wrong'
        }, follow_redirects=True)
        
        self.assertIn(b'Invalid', response.data)
    
    def test_patient_registration(self):
        """Test patient registration"""
        response = self.client.post('/patient/register', data={
            'full_name': 'Test Patient',
            'age': '30',
            'gender': 'Male',
            'phone': '1234567890',
            'email': 'patient@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'address': '123 Test St',
            'blood_group': 'O+',
            'emergency_contact': '0987654321'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)
    
    def test_patient_login_success(self):
        """Test successful patient login"""
        # Register patient first
        with self.app.app_context():
            mysql = MySQL(self.app)
            Patient.create(mysql, 'Test Patient', 30, 'Male', '1234567890',
                          'patient@test.com', 'password123')
        
        # Attempt login
        response = self.client.post('/patient/login', data={
            'email': 'patient@test.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
    
    def test_doctor_login_success(self):
        """Test successful doctor login"""
        # Create doctor
        with self.app.app_context():
            mysql = MySQL(self.app)
            Doctor.create(mysql, 'DOC001', 'password123', 'Dr. Test', 
                         'Test University', 'test@doctor.com', '1234567890',
                         created_by=1)
        
        # Attempt login
        response = self.client.post('/doctor/login', data={
            'doctor_code': 'DOC001',
            'password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        """Test logout functionality"""
        # Login first
        with self.app.app_context():
            mysql = MySQL(self.app)
            Patient.create(mysql, 'Test Patient', 30, 'Male', '1234567890',
                          'patient@test.com', 'password123')
        
        with self.client:
            self.client.post('/patient/login', data={
                'email': 'patient@test.com',
                'password': 'password123'
            })
            
            # Logout
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'logged out', response.data)

if __name__ == '__main__':
    unittest.main()
