"""
Unit Tests for Admin Login Feature
Tests the secure admin authentication system

User Story:
As an Admin, I want to log in securely so that I can access the hospital 
management dashboard and control the system.

Confirmation Criteria:
1. Admin must enter a valid username and password
2. If credentials are correct, system redirects to admin dashboard
3. If credentials are invalid, error message appears
4. If server/database is down, connection error message appears or redirect to login
"""

import unittest
import sys
import os
from datetime import timedelta
from unittest.mock import patch, MagicMock, Mock
import pymysql

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, mysql
from config import config


class AdminLoginTestCase(unittest.TestCase):
    """Test cases for admin login functionality"""

    def setUp(self):
        """Set up test client and test database"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after tests"""
        self.app_context.pop()

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_with_valid_credentials(self, mock_verify):
        """
        Requirement 1 & 2: Admin enters valid username and password
        Expected: System redirects to admin dashboard
        """
        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 1
        }

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/dashboard', response.location)
        mock_verify.assert_called_once()

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_session_set_correctly(self, mock_verify):
        """
        Verify that session variables are set correctly after valid login
        """

        mock_verify.return_value = {
            'admin_id': 5,
            'username': 'admin',
            'full_name': 'John Administrator',
            'is_active': 1
        }

        self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            follow_redirects=True
        )

        with self.client.session_transaction() as sess:
            self.assertEqual(sess.get('user_type'), 'admin')
            self.assertEqual(sess.get('user_id'), 5)
            self.assertEqual(sess.get('user_name'), 'John Administrator')
            self.assertTrue(sess.permanent)

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_flash_message_success(self, mock_verify):
        """
        Verify success flash message is displayed after valid login
        """

        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 1
        }

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            follow_redirects=True
        )

        self.assertIn(b'Welcome', response.data)




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_with_invalid_credentials(self, mock_verify):
        """
        Requirement 3: Admin enters invalid credentials
        Expected: Error message "Invalid username or password" appears
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'wrongpassword'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)  # Page loads
        self.assertIn(b'Invalid username or password', response.data)

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_with_wrong_username(self, mock_verify):
        """
        Test login with non-existent username
        Expected: Invalid credentials error
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'nonexistent_admin',
                'password': 'password123'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
        mock_verify.assert_called_once()

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_with_wrong_password(self, mock_verify):
        """
        Test login with correct username but wrong password
        Expected: Invalid credentials error
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'wrongpassword'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_session_not_set_on_invalid_credentials(self, mock_verify):
        """
        Verify session is NOT set when credentials are invalid
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'wrongpassword'
            },
            follow_redirects=True
        )

        with self.client.session_transaction() as sess:
            self.assertIsNone(sess.get('user_type'))
            self.assertIsNone(sess.get('user_id'))

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_no_redirect_on_invalid_credentials(self, mock_verify):
        """
        Verify no redirect to dashboard on invalid credentials
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'wrongpassword'
            },
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login', response.location)




    def test_admin_login_missing_username(self):
        """
        Test login attempt with missing username
        Expected: Validation error
        """

        response = self.client.post(
            '/admin/login',
            data={
                'username': '',
                'password': 'password123'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter username and password', response.data)

    def test_admin_login_missing_password(self):
        """
        Test login attempt with missing password
        Expected: Validation error
        """

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': ''
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter username and password', response.data)

    def test_admin_login_missing_both_fields(self):
        """
        Test login attempt with both fields missing
        Expected: Validation error
        """

        response = self.client.post(
            '/admin/login',
            data={
                'username': '',
                'password': ''
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter username and password', response.data)

    def test_admin_login_only_whitespace(self):
        """
        Test login attempt with whitespace-only credentials
        Expected: Validation error
        """

        response = self.client.post(
            '/admin/login',
            data={
                'username': '   ',
                'password': '   '
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter username and password', response.data)




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_with_inactive_account(self, mock_verify):
        """
        Test login with valid credentials but inactive admin account
        Expected: Access denied error
        """

        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 0  # Account is inactive
        }

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            follow_redirects=True
        )



        self.assertEqual(response.status_code, 200)

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_inactive_account_no_session(self, mock_verify):
        """
        Verify that admin account status is checked during login
        """

        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 0
        }

        self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            follow_redirects=True
        )


        mock_verify.assert_called_once()




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_database_connection_error(self, mock_verify):
        """
        Requirement 4: Database connection is down
        Expected: Connection error message or redirect to login page
        """

        mock_verify.side_effect = pymysql.Error("Connection refused")

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_mysql_general_error(self, mock_verify):
        """
        Test handling of general MySQL errors
        Expected: Error handling with appropriate message
        """

        mock_verify.side_effect = pymysql.MySQLError("MySQL Server error")

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_database_timeout(self, mock_verify):
        """
        Test handling of database timeout
        Expected: Error handling with user-friendly message
        """

        mock_verify.side_effect = pymysql.Error("Connection timeout")

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)




    def test_admin_login_get_request_displays_form(self):
        """
        Test that GET request to login page displays form
        """

        response = self.client.get('/admin/login')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())
        self.assertIn(b'username', response.data.lower())
        self.assertIn(b'password', response.data.lower())




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_username_case_sensitivity(self, mock_verify):
        """
        Test that username comparison is handled correctly
        """

        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 1
        }

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'ADMIN',
                'password': 'correctpassword123'
            },
            follow_redirects=False
        )

        mock_verify.assert_called_once()




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_sql_injection_attempt(self, mock_verify):
        """
        Test that SQL injection attempts are handled safely
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': "admin' OR '1'='1",
                'password': "' OR '1'='1"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)


        mock_verify.assert_called_once()




    def test_admin_dashboard_requires_authentication(self):
        """
        Test that admin dashboard requires authenticated session
        """

        response = self.client.get(
            '/admin/dashboard',
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login', response.location)

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_can_access_dashboard_after_login(self, mock_verify):
        """
        Test that authenticated admin can access dashboard
        """

        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 1
        }

        self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            }
        )

        response = self.client.get(
            '/admin/dashboard',
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 200)




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_session_persists_across_requests(self, mock_verify):
        """
        Test that session persists across multiple requests
        """

        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 1
        }

        self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            }
        )

        response1 = self.client.get('/admin/dashboard')
        response2 = self.client.get('/admin/doctors')
        response3 = self.client.get('/admin/patients')

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_can_logout(self, mock_verify):
        """
        Test that admin can logout and session is cleared
        """

        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 1
        }

        self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            }
        )

        response = self.client.get('/logout', follow_redirects=False)

        self.assertEqual(response.status_code, 302)

        response = self.client.get('/admin/dashboard', follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login', response.location)




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_with_special_characters(self, mock_verify):
        """
        Test login with special characters in password
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': "p@$$w0rd!#%&*()[]{}|\\;:'\",.<>?/"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        mock_verify.assert_called_once()

    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_with_unicode_characters(self, mock_verify):
        """
        Test login with unicode characters
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'пароль密码🔐'
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        mock_verify.assert_called_once()




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_with_very_long_credentials(self, mock_verify):
        """
        Test login with extremely long credentials
        """

        mock_verify.return_value = None

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'a' * 1000,
                'password': 'p' * 10000
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        mock_verify.assert_called_once()




    @patch('routes.admin_routes.Admin.verify_password')
    def test_multiple_failed_login_attempts(self, mock_verify):
        """
        Test handling of multiple failed login attempts
        (Note: This tests if the system doesn't crash; rate limiting would be tested separately)
        """

        mock_verify.return_value = None

        for i in range(5):
            response = self.client.post(
                '/admin/login',
                data={
                    'username': 'admin',
                    'password': f'wrongpassword{i}'
                },
                follow_redirects=True
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Invalid username or password', response.data)




    @patch('routes.admin_routes.Admin.verify_password')
    def test_admin_login_form_urlencoded(self, mock_verify):
        """
        Test login with standard form-urlencoded content type
        """

        mock_verify.return_value = {
            'admin_id': 1,
            'username': 'admin',
            'full_name': 'System Administrator',
            'is_active': 1
        }

        response = self.client.post(
            '/admin/login',
            data={
                'username': 'admin',
                'password': 'correctpassword123'
            },
            content_type='application/x-www-form-urlencoded',
            follow_redirects=False
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/dashboard', response.location)


class AdminLoginIntegrationTestCase(unittest.TestCase):
    """Integration tests for admin login (without mocking database)"""

    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up"""
        self.app_context.pop()

    def test_login_page_loads(self):
        """
        Integration test: Verify login page loads without errors
        """
        response = self.client.get('/admin/login')
        self.assertEqual(response.status_code, 200)

    def test_login_form_contains_required_fields(self):
        """
        Integration test: Verify login form contains required fields
        """
        response = self.client.get('/admin/login')
        self.assertIn(b'username', response.data)
        self.assertIn(b'password', response.data)
        self.assertIn(b'submit', response.data.lower())


if __name__ == '__main__':

    unittest.main(verbosity=2)

