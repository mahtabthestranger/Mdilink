"""
Test Cases for Al Mamun Oualid's Features
Features: F3, F4, F5
Author: Al Mamun Oualid
"""

import pytest
from app import app
from flask import session


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


# F3: Doctor Login Tests

def test_f3_login_page_loads(client):
    response = client.get('/doctor/login')
    assert response.status_code == 200
    assert b'Doctor Login' in response.data


def test_f3_valid_login(client):
    response = client.post('/doctor/login', data={
        'doctor_code': 'DOC001',
        'password': 'admin123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Welcome' in response.data or b'Dashboard' in response.data


def test_f3_invalid_credentials(client):
    response = client.post('/doctor/login', data={
        'doctor_code': 'WRONG123',
        'password': 'wrongpass'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid credentials' in response.data


def test_f3_empty_fields(client):
    response = client.post('/doctor/login', data={
        'doctor_code': '',
        'password': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Please enter doctor ID and password' in response.data


def test_f3_inactive_account(client):
    # This test would need a doctor with is_active = FALSE in database
    pass


# F4: Doctor Appointments Tests

def test_f4_appointments_page_requires_login(client):
    response = client.get('/doctor/appointments')
    assert response.status_code == 302


def test_f4_appointments_page_with_login(client):
    with client.session_transaction() as sess:
        sess['user_type'] = 'doctor'
        sess['user_id'] = 1
        sess['user_name'] = 'Dr. Test'
    
    response = client.get('/doctor/appointments')
    assert response.status_code == 200


def test_f4_filter_by_date(client):
    with client.session_transaction() as sess:
        sess['user_type'] = 'doctor'
        sess['user_id'] = 1
    
    response = client.get('/doctor/appointments?date=2025-12-01')
    assert response.status_code == 200


def test_f4_filter_by_status(client):
    with client.session_transaction() as sess:
        sess['user_type'] = 'doctor'
        sess['user_id'] = 1
    
    response = client.get('/doctor/appointments?status=Scheduled')
    assert response.status_code == 200


# F5: Medical Records Tests

def test_f5_patients_list_requires_login(client):
    response = client.get('/doctor/patients')
    assert response.status_code == 302


def test_f5_patients_list_with_login(client):
    with client.session_transaction() as sess:
        sess['user_type'] = 'doctor'
        sess['user_id'] = 1
    
    response = client.get('/doctor/patients')
    assert response.status_code == 200


def test_f5_add_record_page_loads(client):
    with client.session_transaction() as sess:
        sess['user_type'] = 'doctor'
        sess['user_id'] = 1
    
    response = client.get('/doctor/patient/1/add-record')
    assert response.status_code == 200 or response.status_code == 404


def test_f5_add_record_validation(client):
    with client.session_transaction() as sess:
        sess['user_type'] = 'doctor'
        sess['user_id'] = 1
    
    response = client.post('/doctor/patient/1/add-record', data={
        'diagnosis': '',
        'symptoms': 'Test symptoms'
    }, follow_redirects=True)
    
    assert b'mandatory' in response.data or b'required' in response.data


# Integration Tests

def test_complete_doctor_workflow(client):
    # Step 1: Login
    response1 = client.post('/doctor/login', data={
        'doctor_code': 'DOC001',
        'password': 'admin123'
    }, follow_redirects=True)
    assert response1.status_code == 200
    
    # Step 2: View appointments
    response2 = client.get('/doctor/appointments')
    assert response2.status_code == 200
    
    # Step 3: View patients
    response3 = client.get('/doctor/patients')
    assert response3.status_code == 200


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

