"""
Patient Authentication Module - Medilink Hospital Management System.

Developer: Mahtab Ahmed

This module provides patient authentication features including
registration, login, dashboard and session management.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from config import Config

import pymysql
pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL
from models.patient import Patient

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

app.config['MYSQL_HOST'] = Config.MYSQL_HOST
app.config['MYSQL_USER'] = Config.MYSQL_USER
app.config['MYSQL_PASSWORD'] = Config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = Config.MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = Config.MYSQL_CURSORCLASS

mysql = MySQL(app)


@app.route('/')
def index():
    """Redirect to patient login page."""
    return redirect(url_for('patient_login'))


@app.route('/patient/register', methods=['GET', 'POST'])
def patient_register():
    """Handle patient registration with form validation."""
    if request.method == 'POST':
        
        full_name = request.form.get('full_name', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        address = request.form.get('address', '').strip()
        blood_group = request.form.get('blood_group', '').strip()
        emergency_contact = request.form.get('emergency_contact', '').strip()

        # Validate required fields
        if not all([full_name, age, gender, phone, email, password]):
            flash('Please fill all required fields', 'error')
            return redirect(url_for('patient_register'))

        # Validate password confirmation
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('patient_register'))

        # Validate password length
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('patient_register'))

        # Check double email
        if Patient.email_exists(mysql, email):
            flash('User already registered with this email', 'error')
            return redirect(url_for('patient_register'))

        # create patient account
        try:
            patient_id = Patient.create(
                mysql=mysql,
                full_name=full_name,
                age=age,
                gender=gender,
                phone=phone,
                email=email,
                password=password,
                address=address if address else None,
                blood_group=blood_group if blood_group else None,
                emergency_contact=emergency_contact if emergency_contact else None
            )

            flash('Registration successful! Please login to continue', 'success')
            return redirect(url_for('patient_login'))

        except Exception as error:
            flash('Registration failed. Please try again', 'error')
            print(f"[ERROR] Registration error: {error}")
            return redirect(url_for('patient_register'))

    return render_template('patient/register.html')


@app.route('/patient/login', methods=['GET', 'POST'])
def patient_login():
    """Handle patient login with session management."""
    if request.method == 'POST':
        # Get login info from form
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Validate 
        if not email or not password:
            flash('Please enter email and password', 'error')
            return redirect(url_for('patient_login'))

        # Verify 
        patient = Patient.verify_password(mysql, email, password)

        if patient:
            #  (Session Management)
            session['user_type'] = 'patient'
            session['user_id'] = patient['patient_id']
            session['user_name'] = patient['full_name']
            session['user_email'] = patient['email']
            session.permanent = True

            flash(f'Welcome back, {patient["full_name"]}!', 'success')
            # Redirect to dashboard
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('patient_login'))

    return render_template('patient/login.html')



@app.route('/patient/dashboard')
def patient_dashboard():
    """Display patient dashboard (protected route)."""
    if session.get('user_type') != 'patient':
        flash('Please login to access patient dashboard', 'error')
        return redirect(url_for('patient_login'))

    return render_template('patient/dashboard.html')


@app.route('/logout')
def logout():
    """Clear session and logout user."""
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('patient_login'))


@app.route('/forgot-password')
def forgot_password():
    """Placeholder for forgot password."""
    return redirect(url_for('patient_login'))


@app.route('/patient/book-appointment')
def patient_book_appointment():
    """Placeholder for book appointment."""
    if session.get('user_type') != 'patient':
        return redirect(url_for('patient_login'))
    return redirect(url_for('patient_dashboard'))


@app.route('/patient/appointments')
def patient_appointments():
    """Placeholder for view appointments."""
    if session.get('user_type') != 'patient':
        return redirect(url_for('patient_login'))
    return redirect(url_for('patient_dashboard'))


@app.route('/patient/medical-records')
def patient_medical_records():
    """Placeholder for medical records."""
    if session.get('user_type') != 'patient':
        return redirect(url_for('patient_login'))
    return redirect(url_for('patient_dashboard'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)

