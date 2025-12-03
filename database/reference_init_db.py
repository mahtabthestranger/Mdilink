"""
Database Initialization Script - Medilink Hospital Management System.

Developer: Mahtab Ahmed
"""

import sys
import os
import pymysql

pymysql.install_as_MySQLdb()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config


def create_database():
    """
    Create the database if it doesn't exist.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB}")
        print(f"[OK] Database '{Config.MYSQL_DB}' created/verified")
        cursor.close()
        conn.close()
        return True
    except Exception as error:
        print(f"[ERROR] Error creating database: {error}")
        return False


def create_tables():
    """
    Create all necessary database tables.

    Creates tables for admins, doctors, patients, appointments,
    medical records, password reset tokens, and chat messages.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cursor = conn.cursor()
        
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
        print("[OK] Table 'admins' created successfully")
        
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
                created_by INT,
                FOREIGN KEY (created_by) REFERENCES admins(admin_id) ON DELETE SET NULL
            )
        """)
        print("[OK] Table 'doctors' created successfully")
        
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
        print("[OK] Table 'patients' created successfully")
        
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
                UNIQUE KEY unique_appointment (doctor_id, appointment_date, appointment_time)
            )
        """)
        print("[OK] Table 'appointments' created successfully")
        
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
                FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE SET NULL
            )
        """)
        print("[OK] Table 'medical_records' created successfully")
        
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
        print("[OK] Table 'password_reset_tokens' created successfully")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                message_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                user_type ENUM('admin', 'doctor', 'patient', 'guest') DEFAULT 'guest',
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("[OK] Table 'chat_messages' created successfully")

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as error:
        print(f"[ERROR] Error creating tables: {error}")
        return False


def seed_admin_data():
    """
    Insert default admin account into the database.

    Creates a default admin user with username 'admin' and
    password 'admin123' if one doesn't already exist.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admins WHERE username = 'admin'")
        if cursor.fetchone():
            print("[INFO] Default admin account already exists")
        else:
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash('admin123')

            cursor.execute("""
                INSERT INTO admins (username, password, full_name, email, phone)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                'admin',
                hashed_password,
                'System Administrator',
                'admin@medilink.com',
                '01700000000'
            ))

            conn.commit()
            print("[OK] Default admin created (username: admin, password: admin123)")

        cursor.close()
        conn.close()
        return True
    except Exception as error:
        print(f"[ERROR] Error seeding admin data: {error}")
        return False


def main():
    """
    Main initialization function.

    Executes database setup in three steps:
        1. Create database
        2. Create tables
        3. Seed initial data
    """
    print("\n" + "=" * 60)
    print("MEDILINK DATABASE INITIALIZATION")
    print("Developer: Mahtab Ahmed")
    print("=" * 60 + "\n")

    print("Step 1: Creating database...")
    if not create_database():
        print("\n[ERROR] Database initialization failed!")
        return

    print("\nStep 2: Creating tables...")
    if not create_tables():
        print("\n[ERROR] Table creation failed!")
        return

    print("\nStep 3: Seeding initial data...")
    if not seed_admin_data():
        print("\n[ERROR] Data seeding failed!")
        return

    print("\n" + "=" * 60)
    print("[OK] DATABASE INITIALIZATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nDefault Admin Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\n[!] Please change the default password after first login!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
