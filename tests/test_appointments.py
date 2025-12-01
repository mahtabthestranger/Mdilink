"""
Unit Tests for Appointment Features
"""

import unittest
from tests.test_base import BaseTestCase
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from flask_mysqldb import MySQL
from datetime import date, time

class TestAppointments(BaseTestCase):
    """Test appointment features"""
    
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
            
            # Create test doctor
            self.doctor_id = Doctor.create(
                mysql, 'DOC001', 'password123', 'Dr. Test',
                'Test University', 'doctor@test.com', '1234567890',
                created_by=1
            )
    
    def test_create_appointment(self):
        """Test creating an appointment"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            appointment_id = Appointment.create(
                mysql, self.patient_id, self.doctor_id,
                date.today(), time(10, 0), 'Checkup'
            )
            
            self.assertIsNotNone(appointment_id)
            self.assertGreater(appointment_id, 0)
    
    def test_get_appointments_by_patient(self):
        """Test retrieving appointments by patient"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            # Create appointment
            Appointment.create(
                mysql, self.patient_id, self.doctor_id,
                date.today(), time(10, 0), 'Checkup'
            )
            
            # Retrieve appointments
            appointments = Appointment.get_by_patient(mysql, self.patient_id)
            
            self.assertEqual(len(appointments), 1)
            self.assertEqual(appointments[0]['reason'], 'Checkup')
    
    def test_get_appointments_by_doctor(self):
        """Test retrieving appointments by doctor"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            # Create appointment
            Appointment.create(
                mysql, self.patient_id, self.doctor_id,
                date.today(), time(10, 0), 'Checkup'
            )
            
            # Retrieve appointments
            appointments = Appointment.get_by_doctor(mysql, self.doctor_id)
            
            self.assertEqual(len(appointments), 1)
    
    def test_filter_appointments_by_status(self):
        """Test filtering appointments by status"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            # Create appointments with different statuses
            appt1 = Appointment.create(
                mysql, self.patient_id, self.doctor_id,
                date.today(), time(10, 0), 'Checkup'
            )
            
            appt2 = Appointment.create(
                mysql, self.patient_id, self.doctor_id,
                date.today(), time(11, 0), 'Follow-up'
            )
            
            # Mark one as completed
            Appointment.update_status(mysql, appt1, 'Completed')
            
            # Filter by status
            scheduled = Appointment.get_by_doctor(mysql, self.doctor_id, status_filter='Scheduled')
            completed = Appointment.get_by_doctor(mysql, self.doctor_id, status_filter='Completed')
            
            self.assertEqual(len(scheduled), 1)
            self.assertEqual(len(completed), 1)
    
    def test_cancel_appointment(self):
        """Test cancelling an appointment"""
        with self.app.app_context():
            mysql = MySQL(self.app)
            
            # Create appointment
            appt_id = Appointment.create(
                mysql, self.patient_id, self.doctor_id,
                date.today(), time(10, 0), 'Checkup'
            )
            
            # Cancel it
            Appointment.update_status(mysql, appt_id, 'Cancelled')
            
            # Verify
            appointment = Appointment.find_by_id(mysql, appt_id)
            self.assertEqual(appointment['status'], 'Cancelled')

if __name__ == '__main__':
    unittest.main()
