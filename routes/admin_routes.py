"""
Admin Routes Module for Medilink Hospital Management System

This module contains all admin-related routes including authentication,
dashboard statistics, and management operations for doctors and patients.

Author: Medilink Development Team
Date: December 2025
"""

from flask import render_template, request, redirect, url_for, session, flash
from models.admin import Admin
from models.doctor import Doctor
from models.patient import Patient


def register_admin_routes(app, mysql):
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')

            if not username or not password:
                flash('Please enter username and password', 'error')
                return redirect(url_for('admin_login'))

            try:
                admin = Admin.verify_password(mysql, username, password)

                if admin:
                    session['user_type'] = 'admin'
                    session['user_id'] = admin['admin_id']
                    session['user_name'] = admin['full_name']
                    session['username'] = admin['username']
                    session.permanent = True

                    flash(
                        f'Welcome, {admin["full_name"]}!',
                        'success'
                    )
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid username or password', 'error')
                    return redirect(url_for('admin_login'))

            except Exception as error:
                print(f'Admin login error: {error}')
                flash('An error occurred during login. Please try again',
                      'error')
                return redirect(url_for('admin_login'))

        return render_template('admin/login.html')




    @app.route('/admin/dashboard')
    def admin_dashboard():
        if session.get('user_type') != 'admin':
            flash('Please login to access admin dashboard', 'error')
            return redirect(url_for('admin_login'))

        try:
            cursor = mysql.connection.cursor()

            cursor.execute(
                "SELECT COUNT(*) as count FROM doctors WHERE is_active = TRUE"
            )
            doctor_count = cursor.fetchone()['count']

            cursor.execute(
                "SELECT COUNT(*) as count FROM patients WHERE is_active = TRUE"
            )
            patient_count = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM appointments")
            appointment_count = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM medical_records")
            record_count = cursor.fetchone()['count']

            cursor.close()

            return render_template(
                'admin/dashboard.html',
                doctor_count=doctor_count,
                patient_count=patient_count,
                appointment_count=appointment_count,
                record_count=record_count
            )

        except Exception as error:
            print(f'Dashboard error: {error}')
            flash('Failed to load dashboard statistics', 'error')
            return redirect(url_for('admin_login'))




    @app.route('/admin/doctors')
    def admin_doctors():
        if session.get('user_type') != 'admin':
            flash('Please login as admin', 'error')
            return redirect(url_for('admin_login'))

        try:
            doctors = Doctor.get_all(mysql)
            return render_template('admin/doctors.html', doctors=doctors)

        except Exception as error:
            print(f'Error fetching doctors: {error}')
            flash('Failed to load doctors list', 'error')
            return redirect(url_for('admin_dashboard'))

    @app.route('/admin/doctors/add', methods=['GET', 'POST'])
    def admin_add_doctor():
        if session.get('user_type') != 'admin':
            flash('Please login as admin', 'error')
            return redirect(url_for('admin_login'))

        if request.method == 'POST':
            doctor_code = request.form.get('doctor_code', '').strip()
            full_name = request.form.get('full_name', '').strip()
            university = request.form.get('university', '').strip()
            specialization = request.form.get('specialization', '').strip()
            qualification = request.form.get('qualification', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            address = request.form.get('address', '').strip()
            password = request.form.get('password', '')

            if not all([doctor_code, full_name, university, email, phone,
                        password]):
                flash('Please fill all required fields', 'error')
                return redirect(url_for('admin_add_doctor'))

            if Doctor.find_by_code(mysql, doctor_code):
                flash('Doctor ID already exists', 'error')
                return redirect(url_for('admin_add_doctor'))

            try:
                doctor_id = Doctor.create(
                    mysql=mysql,
                    doctor_code=doctor_code,
                    password=password,
                    full_name=full_name,
                    university=university,
                    email=email,
                    phone=phone,
                    specialization=(specialization
                                    if specialization else None),
                    qualification=(qualification
                                   if qualification else None),
                    address=address if address else None,
                    created_by=session.get('user_id')
                )

                flash(f'Doctor {full_name} added successfully!', 'success')
                return redirect(url_for('admin_doctors'))

            except Exception as error:
                print(f'Error adding doctor: {error}')
                flash('Failed to add doctor. Please try again', 'error')
                return redirect(url_for('admin_add_doctor'))

        return render_template('admin/add_doctor.html')

    @app.route('/admin/doctors/edit/<int:doctor_id>',
               methods=['GET', 'POST'])
    def admin_edit_doctor(doctor_id):
        if session.get('user_type') != 'admin':
            flash('Please login as admin', 'error')
            return redirect(url_for('admin_login'))

        doctor = Doctor.find_by_id(mysql, doctor_id)
        if not doctor:
            flash('Doctor not found', 'error')
            return redirect(url_for('admin_doctors'))

        if request.method == 'POST':
            full_name = request.form.get('full_name', '').strip()
            university = request.form.get('university', '').strip()
            specialization = request.form.get('specialization', '').strip()
            qualification = request.form.get('qualification', '').strip()
            email = request.form.get('email', '').strip().lower()
            phone = request.form.get('phone', '').strip()
            address = request.form.get('address', '').strip()
            password = request.form.get('password', '')

            if not all([full_name, university, email, phone]):
                flash('Please fill all required fields', 'error')
                return redirect(
                    url_for('admin_edit_doctor', doctor_id=doctor_id)
                )

            try:
                update_data = {
                    'full_name': full_name,
                    'university': university,
                    'email': email,
                    'phone': phone,
                    'specialization': (specialization
                                       if specialization else None),
                    'qualification': (qualification
                                      if qualification else None),
                    'address': address if address else None
                }

                if password:
                    update_data['password'] = password

                Doctor.update(mysql, doctor_id, **update_data)

                flash(f'Doctor {full_name} updated successfully!',
                      'success')
                return redirect(url_for('admin_doctors'))

            except Exception as error:
                print(f'Error updating doctor: {error}')
                flash('Failed to update doctor. Please try again', 'error')
                return redirect(
                    url_for('admin_edit_doctor', doctor_id=doctor_id)
                )

        return render_template('admin/edit_doctor.html', doctor=doctor)

    @app.route('/admin/doctors/delete/<int:doctor_id>', methods=['POST'])
    def admin_delete_doctor(doctor_id):
        if session.get('user_type') != 'admin':
            flash('Please login as admin', 'error')
            return redirect(url_for('admin_login'))

        doctor = Doctor.find_by_id(mysql, doctor_id)
        if not doctor:
            flash('Doctor not found', 'error')
            return redirect(url_for('admin_doctors'))

        try:
            Doctor.delete(mysql, doctor_id)
            flash(f'Doctor {doctor["full_name"]} deleted successfully',
                  'success')

        except Exception as error:
            print(f'Error deleting doctor: {error}')
            flash('Failed to delete doctor', 'error')

        return redirect(url_for('admin_doctors'))




    @app.route('/admin/patients')
    def admin_patients():
        if session.get('user_type') != 'admin':
            flash('Please login as admin', 'error')
            return redirect(url_for('admin_login'))

        try:
            patients = Patient.get_all(mysql)
            return render_template('admin/patients.html',
                                   patients=patients)

        except Exception as error:
            print(f'Error fetching patients: {error}')
            flash('Failed to load patients list', 'error')
            return redirect(url_for('admin_dashboard'))

    @app.route('/admin/patients/edit/<int:patient_id>',
               methods=['GET', 'POST'])
    def admin_edit_patient(patient_id):
        if session.get('user_type') != 'admin':
            flash('Please login as admin', 'error')
            return redirect(url_for('admin_login'))

        patient = Patient.find_by_id(mysql, patient_id)
        if not patient:
            flash('Patient not found', 'error')
            return redirect(url_for('admin_patients'))

        if request.method == 'POST':
            full_name = request.form.get('full_name', '').strip()
            age = request.form.get('age', '').strip()
            gender = request.form.get('gender', '').strip()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip().lower()
            address = request.form.get('address', '').strip()
            blood_group = request.form.get('blood_group', '').strip()
            emergency_contact = (
                request.form.get('emergency_contact', '').strip()
            )

            if not all([full_name, age, gender, phone, email]):
                flash('Please fill all required fields', 'error')
                return redirect(
                    url_for('admin_edit_patient', patient_id=patient_id)
                )

            try:
                Patient.update(
                    mysql=mysql,
                    patient_id=patient_id,
                    full_name=full_name,
                    age=age,
                    gender=gender,
                    phone=phone,
                    email=email,
                    address=address if address else None,
                    blood_group=blood_group if blood_group else None,
                    emergency_contact=(emergency_contact
                                       if emergency_contact else None)
                )

                flash(f'Patient {full_name} updated successfully!',
                      'success')
                return redirect(url_for('admin_patients'))

            except Exception as error:
                print(f'Error updating patient: {error}')
                flash('Failed to update patient. Please try again', 'error')
                return redirect(
                    url_for('admin_edit_patient', patient_id=patient_id)
                )

        return render_template('admin/edit_patient.html', patient=patient)

    @app.route('/admin/patients/delete/<int:patient_id>', methods=['POST'])
    def admin_delete_patient(patient_id):
        if session.get('user_type') != 'admin':
            flash('Please login as admin', 'error')
            return redirect(url_for('admin_login'))

        patient = Patient.find_by_id(mysql, patient_id)
        if not patient:
            flash('Patient not found', 'error')
            return redirect(url_for('admin_patients'))

        try:
            Patient.delete(mysql, patient_id)
            flash(f'Patient {patient["full_name"]} deleted successfully',
                  'success')

        except Exception as error:
            print(f'Error deleting patient: {error}')
            flash('Failed to delete patient', 'error')

        return redirect(url_for('admin_patients'))

