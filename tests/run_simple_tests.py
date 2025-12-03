"""
Simplified Unit Tests - Direct Database Connection
Run with: python tests/run_simple_tests.py
"""

import pymysql
import sys
import os
from datetime import date, time, datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Test configuration
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_DB = 'medilink_test_db'

def get_connection():
    """Get database connection"""
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

def setup_database():
    """Create test database and tables"""
    print("\n" + "="*60)
    print("SETTING UP TEST DATABASE")
    print("="*60)
    
    # Create database
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_DB}")
    cursor.execute(f"CREATE DATABASE {MYSQL_DB}")
    cursor.close()
    conn.close()
    print(f"[OK] Created database: {MYSQL_DB}")
    
    # Create tables
    conn = get_connection()
    cursor = conn.cursor()
    
    # Admins table
    cursor.execute("""
        CREATE TABLE admins (
            admin_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(15),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Doctors table
    cursor.execute("""
        CREATE TABLE doctors (
            doctor_id INT AUTO_INCREMENT PRIMARY KEY,
            doctor_code VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            university VARCHAR(100) NOT NULL,
            specialization VARCHAR(100),
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(15) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Patients table
    cursor.execute("""
        CREATE TABLE patients (
            patient_id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            gender ENUM('Male', 'Female', 'Other') NOT NULL,
            phone VARCHAR(15) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    """)
    
    # Appointments table
    cursor.execute("""
        CREATE TABLE appointments (
            appointment_id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT NOT NULL,
            doctor_id INT NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            status ENUM('Scheduled', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Password reset tokens table
    cursor.execute("""
        CREATE TABLE password_reset_tokens (
            token_id INT AUTO_INCREMENT PRIMARY KEY,
            user_type ENUM('admin', 'doctor', 'patient') NOT NULL,
            user_id INT NOT NULL,
            email VARCHAR(100) NOT NULL,
            token VARCHAR(255) UNIQUE NOT NULL,
            expires_at DATETIME NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("[OK] Created all tables")
    print("="*60 + "\n")

def cleanup_database():
    """Drop test database"""
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {MYSQL_DB}")
    cursor.close()
    conn.close()
    print(f"\n[OK] Cleaned up test database: {MYSQL_DB}\n")

def clear_tables():
    """Clear all data from tables"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in ['password_reset_tokens', 'appointments', 'patients', 'doctors', 'admins']:
        cursor.execute(f"TRUNCATE TABLE {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    cursor.close()
    conn.close()

# ==================== TESTS ====================

def test_patient_registration():
    """Test patient registration"""
    print("TEST: Patient Registration... ", end="")
    clear_tables()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create patient
    hashed_password = generate_password_hash("password123")
    cursor.execute("""
        INSERT INTO patients (full_name, age, gender, phone, email, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, ("Test Patient", 30, "Male", "1234567890", "patient@test.com", hashed_password))
    conn.commit()
    patient_id = cursor.lastrowid
    
    # Verify
    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    patient = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    assert patient is not None, "Patient not created"
    assert patient['email'] == "patient@test.com", "Email mismatch"
    assert check_password_hash(patient['password'], "password123"), "Password not hashed correctly"
    print("[OK] PASSED")

def test_patient_login():
    """Test patient login"""
    print("TEST: Patient Login... ", end="")
    clear_tables()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create patient
    hashed_password = generate_password_hash("password123")
    cursor.execute("""
        INSERT INTO patients (full_name, age, gender, phone, email, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, ("Test Patient", 30, "Male", "1234567890", "patient@test.com", hashed_password))
    conn.commit()
    
    # Attempt login
    cursor.execute("SELECT * FROM patients WHERE email = %s", ("patient@test.com",))
    patient = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    assert patient is not None, "Patient not found"
    assert check_password_hash(patient['password'], "password123"), "Password verification failed"
    print("[OK] PASSED")

def test_create_appointment():
    """Test creating an appointment"""
    print("TEST: Create Appointment... ", end="")
    clear_tables()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create patient and doctor
    hashed_password = generate_password_hash("password123")
    cursor.execute("""
        INSERT INTO patients (full_name, age, gender, phone, email, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, ("Test Patient", 30, "Male", "1234567890", "patient@test.com", hashed_password))
    patient_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO doctors (doctor_code, password, full_name, university, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, ("DOC001", hashed_password, "Dr. Test", "Test University", "doctor@test.com", "1234567890"))
    doctor_id = cursor.lastrowid
    
    # Create appointment
    cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason)
        VALUES (%s, %s, %s, %s, %s)
    """, (patient_id, doctor_id, date.today(), time(10, 0), "Checkup"))
    appointment_id = cursor.lastrowid
    conn.commit()
    
    # Verify
    cursor.execute("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id,))
    appointment = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    assert appointment is not None, "Appointment not created"
    assert appointment['status'] == "Scheduled", "Status should be Scheduled"
    assert appointment['reason'] == "Checkup", "Reason mismatch"
    print("[OK] PASSED")

def test_cancel_appointment():
    """Test cancelling an appointment"""
    print("TEST: Cancel Appointment... ", end="")
    clear_tables()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create patient, doctor, and appointment
    hashed_password = generate_password_hash("password123")
    cursor.execute("""
        INSERT INTO patients (full_name, age, gender, phone, email, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, ("Test Patient", 30, "Male", "1234567890", "patient@test.com", hashed_password))
    patient_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO doctors (doctor_code, password, full_name, university, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, ("DOC001", hashed_password, "Dr. Test", "Test University", "doctor@test.com", "1234567890"))
    doctor_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, reason)
        VALUES (%s, %s, %s, %s, %s)
    """, (patient_id, doctor_id, date.today(), time(10, 0), "Checkup"))
    appointment_id = cursor.lastrowid
    conn.commit()
    
    # Cancel appointment
    cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE appointment_id = %s", (appointment_id,))
    conn.commit()
    
    # Verify
    cursor.execute("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id,))
    appointment = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    assert appointment['status'] == "Cancelled", "Status should be Cancelled"
    print("[OK] PASSED")

def test_password_reset_token():
    """Test password reset token creation and verification"""
    print("TEST: Password Reset Token... ", end="")
    clear_tables()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create patient
    hashed_password = generate_password_hash("password123")
    cursor.execute("""
        INSERT INTO patients (full_name, age, gender, phone, email, password)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, ("Test Patient", 30, "Male", "1234567890", "patient@test.com", hashed_password))
    patient_id = cursor.lastrowid
    conn.commit()
    
    # Create reset token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=1)
    cursor.execute("""
        INSERT INTO password_reset_tokens (user_type, user_id, email, token, expires_at)
        VALUES (%s, %s, %s, %s, %s)
    """, ("patient", patient_id, "patient@test.com", token, expires_at))
    conn.commit()
    
    # Verify token
    cursor.execute("SELECT * FROM password_reset_tokens WHERE token = %s", (token,))
    token_data = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    assert token_data is not None, "Token not created"
    assert token_data['user_type'] == "patient", "User type mismatch"
    assert token_data['email'] == "patient@test.com", "Email mismatch"
    print("[OK] PASSED")

# ==================== MAIN ====================

if __name__ == "__main__":
    try:
        setup_database()
        
        print("RUNNING TESTS")
        print("="*60)
        
        # Run all tests
        test_patient_registration()
        test_patient_login()
        test_create_appointment()
        test_cancel_appointment()
        test_password_reset_token()
        
        print("="*60)
        print("[OK] ALL TESTS PASSED!")
        print("="*60)
        
    except AssertionError as e:
        print(f"[FAIL] FAILED: {e}")
    except Exception as e:
        print(f"[ERROR] ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup_database()

