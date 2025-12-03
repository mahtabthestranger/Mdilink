"""
Medilink Hospital Management System
Main Flask Application
"""

import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import config
import os
from datetime import datetime

app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

class MySQL:
    def __init__(self, app=None):
        self.app = app
        self._connection = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        self.app = app
    
    @property
    def connection(self):
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(
                host=self.app.config.get('MYSQL_HOST', 'localhost'),
                user=self.app.config.get('MYSQL_USER', 'root'),
                password=self.app.config.get('MYSQL_PASSWORD', ''),
                database=self.app.config.get('MYSQL_DB', 'medilink'),
                cursorclass=pymysql.cursors.DictCursor
            )
        return self._connection

mysql = MySQL(app)

from models.admin import Admin
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.password_reset import PasswordReset

from routes.admin_routes import register_admin_routes

register_admin_routes(app, mysql)

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    """Doctor login page"""
    if request.method == 'POST':
        doctor_code = request.form.get('doctor_code', '').strip()
        password = request.form.get('password', '')
        
        if not doctor_code or not password:
            flash('Please enter doctor ID and password', 'error')
            return redirect(url_for('doctor_login'))
        
        doctor = Doctor.verify_password(mysql, doctor_code, password)
        
        if doctor:
            if not doctor.get('is_active', True):
                flash('Access denied. Your account has been deactivated', 'error')
                return redirect(url_for('doctor_login'))
            
            session['user_type'] = 'doctor'
            session['user_id'] = doctor['doctor_id']
            session['user_name'] = doctor['full_name']
            session['doctor_code'] = doctor['doctor_code']
            session.permanent = True
            
            flash(f'Welcome, Dr. {doctor["full_name"]}!', 'success')
            return redirect(url_for('doctor_dashboard'))
        else:
            flash('Invalid credentials', 'error')
            return redirect(url_for('doctor_login'))
    
    return render_template('doctor/login.html')

@app.route('/patient/login', methods=['GET', 'POST'])
def patient_login():
    """Patient login page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please enter email and password', 'error')
            return redirect(url_for('patient_login'))
        
        patient = Patient.verify_password(mysql, email, password)
        
        if patient:
            session['user_type'] = 'patient'
            session['user_id'] = patient['patient_id']
            session['user_name'] = patient['full_name']
            session['user_email'] = patient['email']
            session.permanent = True
            
            flash(f'Welcome back, {patient["full_name"]}!', 'success')
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('patient_login'))
    
    return render_template('patient/login.html')

@app.route('/patient/register', methods=['GET', 'POST'])
def patient_register():
    """Patient registration page"""
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
        
        if not all([full_name, age, gender, phone, email, password]):
            flash('Please fill all required fields', 'error')
            return redirect(url_for('patient_register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('patient_register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('patient_register'))
        
        try:
            age = int(age)
            if age < 1 or age > 150:
                flash('Please enter a valid age', 'error')
                return redirect(url_for('patient_register'))
        except ValueError:
            flash('Please enter a valid age', 'error')
            return redirect(url_for('patient_register'))
        
        if Patient.email_exists(mysql, email):
            flash('User already registered with this email', 'error')
            return redirect(url_for('patient_register'))
        
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
            
        except Exception as e:
            flash('Registration failed. Please try again', 'error')
            print(f"Registration error: {e}")
            return redirect(url_for('patient_register'))
    
    return render_template('patient/register.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user_type = request.form.get('user_type', '').strip()
        
        if not email or not user_type:
            flash('Please enter your email and select user type', 'error')
            return redirect(url_for('forgot_password'))
        
        user = PasswordReset.find_user_by_email(mysql, email, user_type)
        
        if user:
            token = PasswordReset.create_token(mysql, user_type, user['user_id'], email)
            
            reset_link = url_for('reset_password', token=token, _external=True)
            print(f"\n{'='*60}")
            print(f"PASSWORD RESET LINK FOR {user['full_name']} ({email}):")
            print(f"{reset_link}")
            print(f"{'='*60}\n")
            
            flash('Password reset link has been generated. Check the console for the link.', 'success')
        else:

            flash('If an account exists with that email, a reset link has been sent.', 'info')
        
        return redirect(url_for('forgot_password'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""

    token_data = PasswordReset.verify_token(mysql, token)
    
    if not token_data:
        flash('Invalid or expired reset link', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not password or not confirm_password:
            flash('Please enter and confirm your password', 'error')
            return redirect(url_for('reset_password', token=token))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('reset_password', token=token))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('reset_password', token=token))
        
        try:
            from werkzeug.security import generate_password_hash
            hashed_password = generate_password_hash(password)
            
            cursor = mysql.connection.cursor()
            
            if token_data['user_type'] == 'patient':
                cursor.execute("""
                    UPDATE patients SET password = %s WHERE patient_id = %s
                """, (hashed_password, token_data['user_id']))
            elif token_data['user_type'] == 'doctor':
                cursor.execute("""
                    UPDATE doctors SET password = %s WHERE doctor_id = %s
                """, (hashed_password, token_data['user_id']))
            elif token_data['user_type'] == 'admin':
                cursor.execute("""
                    UPDATE admins SET password = %s WHERE admin_id = %s
                """, (hashed_password, token_data['user_id']))
            
            mysql.connection.commit()
            cursor.close()
            
            PasswordReset.delete_token(mysql, token)
            
            flash('Password reset successful! Please login with your new password.', 'success')
            
            if token_data['user_type'] == 'patient':
                return redirect(url_for('patient_login'))
            elif token_data['user_type'] == 'doctor':
                return redirect(url_for('doctor_login'))
            else:
                return redirect(url_for('admin_login'))
                
        except Exception as e:
            flash('Failed to reset password. Please try again.', 'error')
            print(f"Password reset error: {e}")
            return redirect(url_for('reset_password', token=token))
    
    return render_template('reset_password.html', token=token, email=token_data['email'])

@app.route('/logout')
def logout():
    """Logout user"""
    user_type = session.get('user_type')
    session.clear()
    flash('You have been logged out successfully', 'success')
    
    if user_type == 'admin':
        return redirect(url_for('admin_login'))
    elif user_type == 'doctor':
        return redirect(url_for('doctor_login'))
    else:
        return redirect(url_for('patient_login'))

@app.route('/doctor/dashboard')
def doctor_dashboard():
    """Doctor dashboard"""
    if session.get('user_type') != 'doctor':
        flash('Please login to access doctor dashboard', 'error')
        return redirect(url_for('doctor_login'))
    return render_template('doctor/dashboard.html')

@app.route('/doctor/appointments')
def doctor_appointments():
    """View doctor appointments"""
    if session.get('user_type') != 'doctor':
        flash('Please login to access doctor dashboard', 'error')
        return redirect(url_for('doctor_login'))
    
    date_filter = request.args.get('date')
    status_filter = request.args.get('status')
    
    appointments = Appointment.get_by_doctor(mysql, session.get('user_id'), date_filter, status_filter)
    
    from datetime import date
    return render_template('doctor/appointments.html', 
                         appointments=appointments,
                         today_date=date.today().strftime('%Y-%m-%d'),
                         current_date=date_filter,
                         current_status=status_filter)

@app.route('/doctor/appointment/<int:appointment_id>/status', methods=['POST'])
def doctor_update_appointment_status(appointment_id):
    """Update appointment status"""
    if session.get('user_type') != 'doctor':
        flash('Please login to access doctor dashboard', 'error')
        return redirect(url_for('doctor_login'))
    
    status = request.form.get('status')
    if status not in ['Completed', 'Cancelled']:
        flash('Invalid status', 'error')
        return redirect(url_for('doctor_appointments'))
    
    try:
        appointment = Appointment.find_by_id(mysql, appointment_id)
        if not appointment or appointment['doctor_id'] != session.get('user_id'):
            flash('Appointment not found or access denied', 'error')
            return redirect(url_for('doctor_appointments'))
        
        Appointment.update_status(mysql, appointment_id, status)
        flash(f'Appointment marked as {status}', 'success')
        
    except Exception as e:
        flash('Failed to update status', 'error')
        print(f"Error updating status: {e}")
        
    return redirect(url_for('doctor_appointments'))

@app.route('/doctor/patients')
def doctor_patients():
    """List all patients for doctor"""
    if session.get('user_type') != 'doctor':
        flash('Please login to access doctor dashboard', 'error')
        return redirect(url_for('doctor_login'))
    
    patients = Patient.get_all(mysql)
    return render_template('doctor/patients.html', patients=patients)

@app.route('/doctor/patient/<int:patient_id>')
def doctor_view_patient(patient_id):
    """View patient details and history"""
    if session.get('user_type') != 'doctor':
        flash('Please login to access doctor dashboard', 'error')
        return redirect(url_for('doctor_login'))
    
    patient = Patient.find_by_id(mysql, patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('doctor_patients'))
    
    records = MedicalRecord.get_by_patient(mysql, patient_id)
    
    return render_template('doctor/patient_details.html', patient=patient, records=records)

@app.route('/doctor/patient/<int:patient_id>/add-record', methods=['GET', 'POST'])
def doctor_add_record(patient_id):
    """Add new medical record"""
    if session.get('user_type') != 'doctor':
        flash('Please login to access doctor dashboard', 'error')
        return redirect(url_for('doctor_login'))
    
    patient = Patient.find_by_id(mysql, patient_id)
    if not patient:
        flash('Patient not found', 'error')
        return redirect(url_for('doctor_patients'))
    
    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis', '').strip()
        symptoms = request.form.get('symptoms', '').strip()
        prescription = request.form.get('prescription', '').strip()
        tests_recommended = request.form.get('tests_recommended', '').strip()
        notes = request.form.get('notes', '').strip()
        follow_up_date = request.form.get('follow_up_date')
        
        if not diagnosis:
            flash('Diagnosis is required', 'error')
            return redirect(url_for('doctor_add_record', patient_id=patient_id))
        
        try:
            from datetime import date
            MedicalRecord.create(
                mysql=mysql,
                patient_id=patient_id,
                doctor_id=session.get('user_id'),
                visit_date=date.today(),
                diagnosis=diagnosis,
                symptoms=symptoms if symptoms else None,
                prescription=prescription if prescription else None,
                tests_recommended=tests_recommended if tests_recommended else None,
                notes=notes if notes else None,
                follow_up_date=follow_up_date if follow_up_date else None
            )
            
            flash('Medical record added successfully', 'success')
            return redirect(url_for('doctor_view_patient', patient_id=patient_id))
            
        except Exception as e:
            flash('Failed to add medical record', 'error')
            print(f"Error adding record: {e}")
            return redirect(url_for('doctor_add_record', patient_id=patient_id))
    
    return render_template('doctor/add_record.html', patient=patient)

@app.route('/doctor/record/<int:record_id>/edit', methods=['GET', 'POST'])
def doctor_edit_record(record_id):
    """Edit medical record"""
    if session.get('user_type') != 'doctor':
        flash('Please login to access doctor dashboard', 'error')
        return redirect(url_for('doctor_login'))
    
    record = MedicalRecord.find_by_id(mysql, record_id)
    if not record:
        flash('Record not found', 'error')
        return redirect(url_for('doctor_patients'))
    
    if record['doctor_id'] != session.get('user_id'):
        flash('You can only edit records created by you', 'error')
        return redirect(url_for('doctor_view_patient', patient_id=record['patient_id']))
    
    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis', '').strip()
        symptoms = request.form.get('symptoms', '').strip()
        prescription = request.form.get('prescription', '').strip()
        tests_recommended = request.form.get('tests_recommended', '').strip()
        notes = request.form.get('notes', '').strip()
        follow_up_date = request.form.get('follow_up_date')
        
        if not diagnosis:
            flash('Diagnosis is required', 'error')
            return redirect(url_for('doctor_edit_record', record_id=record_id))
        
        try:
            MedicalRecord.update(
                mysql=mysql,
                record_id=record_id,
                diagnosis=diagnosis,
                symptoms=symptoms if symptoms else None,
                prescription=prescription if prescription else None,
                tests_recommended=tests_recommended if tests_recommended else None,
                notes=notes if notes else None,
                follow_up_date=follow_up_date if follow_up_date else None
            )
            
            flash('Medical record updated successfully', 'success')
            return redirect(url_for('doctor_view_patient', patient_id=record['patient_id']))
            
        except Exception as e:
            flash('Failed to update medical record', 'error')
            print(f"Error updating record: {e}")
            return redirect(url_for('doctor_edit_record', record_id=record_id))
            
    return render_template('doctor/edit_record.html', record=record)

@app.route('/patient/dashboard')
def patient_dashboard():
    """Patient dashboard"""
    if session.get('user_type') != 'patient':
        flash('Please login to access patient dashboard', 'error')
        return redirect(url_for('patient_login'))
    return render_template('patient/dashboard.html')

@app.route('/patient/book-appointment', methods=['GET', 'POST'])
def patient_book_appointment():
    """Book an appointment"""
    if session.get('user_type') != 'patient':
        flash('Please login to book an appointment', 'error')
        return redirect(url_for('patient_login'))
    
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        reason = request.form.get('reason', '').strip()

        if not all([doctor_id, appointment_date, appointment_time]):
            flash('Please fill all required fields', 'error')
            return redirect(url_for('patient_book_appointment'))
        
        if not Appointment.check_availability(mysql, doctor_id, appointment_date, appointment_time):
            flash('This time slot is already booked. Please choose another time.', 'error')
            return redirect(url_for('patient_book_appointment'))
        
        try:
            Appointment.create(
                mysql=mysql,
                patient_id=session.get('user_id'),
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason
            )
            
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('patient_dashboard'))
            
        except Exception as e:
            flash('Failed to book appointment. Please try again', 'error')
            print(f"Booking error: {e}")
            return redirect(url_for('patient_book_appointment'))
    
    from datetime import date
    doctors = Doctor.get_all(mysql)
    return render_template('patient/book_appointment.html', 
                         doctors=doctors, 
                         today_date=date.today().strftime('%Y-%m-%d'))

@app.route('/patient/appointments')
def patient_appointments():
    """View patient appointments"""
    if session.get('user_type') != 'patient':
        flash('Please login to view appointments', 'error')
        return redirect(url_for('patient_login'))
    
    appointments = Appointment.get_by_patient(mysql, session.get('user_id'))
    return render_template('patient/appointments.html', appointments=appointments)

@app.route('/patient/appointment/<int:appointment_id>/cancel', methods=['POST'])
def patient_cancel_appointment(appointment_id):
    """Cancel patient appointment"""
    if session.get('user_type') != 'patient':
        flash('Please login to cancel appointments', 'error')
        return redirect(url_for('patient_login'))
    
    try:
        appointment = Appointment.find_by_id(mysql, appointment_id)
        if not appointment or appointment['patient_id'] != session.get('user_id'):
            flash('Appointment not found or access denied', 'error')
            return redirect(url_for('patient_appointments'))
        
        if appointment['status'] != 'Scheduled':
            flash('Only scheduled appointments can be cancelled', 'error')
            return redirect(url_for('patient_appointments'))
        
        Appointment.update_status(mysql, appointment_id, 'Cancelled')
        flash('Appointment cancelled successfully', 'success')
        
    except Exception as e:
        flash('Failed to cancel appointment', 'error')
        print(f"Error cancelling appointment: {e}")
        
    return redirect(url_for('patient_appointments'))

@app.route('/patient/medical-records')
def patient_medical_records():
    """View patient medical records"""
    if session.get('user_type') != 'patient':
        flash('Please login to view medical records', 'error')
        return redirect(url_for('patient_login'))
    
    records = MedicalRecord.get_by_patient(mysql, session.get('user_id'))
    return render_template('patient/medical_records.html', records=records)

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('errors/500.html'), 500

@app.context_processor
def inject_user():
    """Inject user data into all templates"""
    return dict(
        user_type=session.get('user_type'),
        user_id=session.get('user_id'),
        user_name=session.get('user_name')
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

