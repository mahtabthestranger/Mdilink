"""
Unit Tests for Medilink Hospital Management System
Run with: python -m pytest tests/ -v
or: python -m unittest discover tests
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from werkzeug.security import generate_password_hash
import pymysql

class TestConfig:
    """Test configuration"""
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = 'medilink_test_db'
    SECRET_KEY = 'test-secret-key'
    TESTING = True

class BaseTestCase(unittest.TestCase):
    """Base test case with database setup"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database once for all tests"""
        app.config.from_object(TestConfig)
        cls.app = app
        cls.client = app.test_client()
        cls.create_test_database()
    
    @classmethod
    def create_test_database(cls):
        """Create test database and tables"""
        try:
            # Create database
            conn = pymysql.connect(
                host=TestConfig.MYSQL_HOST,
                user=TestConfig.MYSQL_USER,
                password=TestConfig.MYSQL_PASSWORD
            )
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {TestConfig.MYSQL_DB}")
            cursor.execute(f"CREATE DATABASE {TestConfig.MYSQL_DB}")
            cursor.close()
            conn.close()
            
            # Create tables directly
            conn = pymysql.connect(
                host=TestConfig.MYSQL_HOST,
                user=TestConfig.MYSQL_USER,
                password=TestConfig.MYSQL_PASSWORD,
                db=TestConfig.MYSQL_DB
            )
            cursor = conn.cursor()
            
            # Create all tables
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    admin_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(15),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS doctors (
                    doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                    doctor_code VARCHAR(20) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    university VARCHAR(100) NOT NULL,
                    specialization VARCHAR(100),
                    qualification VARCHAR(255),
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(15) NOT NULL,
                    address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_by INT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    age INT NOT NULL,
                    gender ENUM('Male', 'Female', 'Other') NOT NULL,
                    phone VARCHAR(15) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    address TEXT,
                    blood_group VARCHAR(5),
                    emergency_contact VARCHAR(15),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    doctor_id INT NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status ENUM('Scheduled', 'Completed', 'Cancelled', 'No-Show') DEFAULT 'Scheduled',
                    reason TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS medical_records (
                    record_id INT AUTO_INCREMENT PRIMARY KEY,
                    patient_id INT NOT NULL,
                    doctor_id INT NOT NULL,
                    appointment_id INT,
                    visit_date DATE NOT NULL,
                    diagnosis TEXT NOT NULL,
                    symptoms TEXT,
                    prescription TEXT,
                    tests_recommended TEXT,
                    follow_up_date DATE,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_reset_tokens (
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
            
        except Exception as e:
            print(f"Error creating test database: {e}")
            raise
    
    def setUp(self):
        """Set up before each test"""
        self.clear_database()
    
    def clear_database(self):
        """Clear all data from tables"""
        conn = pymysql.connect(
            host=TestConfig.MYSQL_HOST,
            user=TestConfig.MYSQL_USER,
            password=TestConfig.MYSQL_PASSWORD,
            db=TestConfig.MYSQL_DB
        )
        cursor = conn.cursor()
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Clear tables
        tables = ['password_reset_tokens', 'medical_records', 'appointments', 
                  'patients', 'doctors', 'admins']
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table}")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        conn.commit()
        cursor.close()
        conn.close()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        try:
            conn = pymysql.connect(
                host=TestConfig.MYSQL_HOST,
                user=TestConfig.MYSQL_USER,
                password=TestConfig.MYSQL_PASSWORD
            )
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {TestConfig.MYSQL_DB}")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error dropping test database: {e}")

if __name__ == '__main__':
    unittest.main()
