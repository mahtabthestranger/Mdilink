"""
Al Mamun Oualid - Doctor Features Standalone Application
Runs only F3, F4, F5 features independently
"""

import pymysql
# Use PyMySQL as MySQLdb for Windows compatibility
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from config import config
import os
import logging
from datetime import date, datetime

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize MySQL
mysql = MySQL(app)

# Import models
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment
from models.medical_record import MedicalRecord
from models.chatbot import Chatbot


# Chatbot API Route
@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chatbot messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get user context
        user_context = None
        if session.get('user_type'):
            user_context = {
                'user_type': session.get('user_type'),
                'user_id': session.get('user_id'),
                'user_name': session.get('user_name', 'User')
            }
        
        # Get chatbot response
        response = Chatbot.get_response(message, user_context)
        
        # Save to database if user is logged in
        if user_context:
            Chatbot.save_message(
                mysql,
                user_context['user_id'],
                user_context['user_type'],
                message,
                response
            )
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Chat error: {e}")
        return jsonify({'error': 'Failed to process message'}), 500


@app.route('/')
def index():
    """Home page redirects to doctor login"""
    return redirect(url_for('doctor_login'))


@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    """Doctor login page"""
    if request.method == 'POST':
        doctor_code = request.form.get('doctor_code', '').strip()
        password = request.form.get('password', '')
        
        # Validation
        if not doctor_code or not password:
            flash('Please enter doctor ID and password', 'error')
            return redirect(url_for('doctor_login'))
        
        # Verify credentials
        doctor = Doctor.verify_password(mysql, doctor_code, password)
        
        if doctor:
            # Check if account is active
            if not doctor.get('is_active', True):
                flash('Access denied. Your account has been deactivated', 'error')
                return redirect(url_for('doctor_login'))
            
            # Set session
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
    
    # Get filters
    date_filter = request.args.get('date')
    status_filter = request.args.get('status')
    
    appointments = Appointment.get_by_doctor(
        mysql,
        session.get('user_id'),
        date_filter,
        status_filter
    )
    
    return render_template(
        'doctor/appointments.html',
        appointments=appointments,
        today_date=date.today().strftime('%Y-%m-%d'),
        current_date=date_filter,
        current_status=status_filter
    )


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
        # Verify appointment belongs to doctor
        appointment = Appointment.find_by_id(mysql, appointment_id)
        if not appointment or appointment['doctor_id'] != session.get('user_id'):
            flash('Appointment not found or access denied', 'error')
            return redirect(url_for('doctor_appointments'))
        
        Appointment.update_status(mysql, appointment_id, status)
        flash(f'Appointment marked as {status}', 'success')
        
    except Exception as e:
        flash('Failed to update status', 'error')
        logging.error(f"Error updating status: {e}")
        
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
    
    # Get medical history
    records = MedicalRecord.get_by_patient(mysql, patient_id)
    
    return render_template(
        'doctor/patient_details.html',
        patient=patient,
        records=records
    )


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
            logging.error(f"Error adding record: {e}")
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
    
    # Check if this doctor created the record
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
            logging.error(f"Error updating record: {e}")
            return redirect(url_for('doctor_edit_record', record_id=record_id))
            
    return render_template('doctor/edit_record.html', record=record)


@app.route('/forgot-password')
def forgot_password():
    """Forgot password placeholder"""
    flash('Password reset is not available in this demo', 'info')
    return redirect(url_for('doctor_login'))


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('doctor_login'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
