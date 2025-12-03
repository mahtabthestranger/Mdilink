import unittest
import pymysql
pymysql.install_as_MySQLdb()
from Mahtabapp import app


class TestConfig:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'medilink_test_db'
    SECRET_KEY = 'test-secret-key'
    TESTING = True


class TestPatientRegistration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config.from_object(TestConfig)
        cls.app = app
        cls.client = app.test_client()

        try:
            conn = pymysql.connect(host='localhost', user='root', password='')
            cursor = conn.cursor()
            cursor.execute("DROP DATABASE IF EXISTS medilink_test_db")
            cursor.execute("CREATE DATABASE medilink_test_db")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"DB Error: {e}")

        try:
            conn = pymysql.connect(host='localhost', user='root', password='', database='medilink_test_db')
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE patients (
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
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Table Error: {e}")

    def setUp(self):
        try:
            conn = pymysql.connect(host='localhost', user='root', password='', database='medilink_test_db')
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE patients")
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Clear Error: {e}")

    def test_registration_success(self):
        test_patient = {
            'full_name': 'Mahtab Ahmed',
            'age': '23',
            'gender': 'Male',
            'phone': '01354567890',
            'email': 'mahtab@test.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        response = self.client.post('/patient/register', data=test_patient, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        try:
            conn = pymysql.connect(host='localhost', user='root', password='')
            cursor = conn.cursor()
            cursor.execute("DROP DATABASE IF EXISTS medilink_test_db")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Cleanup Error: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)

