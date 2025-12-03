# F8,F9: Patient Features by Maahier A Haai
# F8: Patient Appointment Booking (SRS F8)
# F9: Patient Dashboard & Medical Records (SRS F9)


#F8 codes below

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

        # Validation
        if not all([doctor_id, appointment_date, appointment_time]):
            flash('Please fill all required fields', 'error')
            return redirect(url_for('patient_book_appointment'))

        # Check availability
        if not Appointment.check_availability(mysql, doctor_id, appointment_date, appointment_time):
            flash('This time slot is already booked. Please choose another time.', 'error')
            return redirect(url_for('patient_book_appointment'))

        try:
            # Create appointment
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

    # GET request: Show form
    from datetime import date
    doctors = Doctor.get_all(mysql)
    return render_template('patient/book_appointment.html',
                           doctors=doctors,
                           today_date=date.today().strftime('%Y-%m-%d'))



#F9 Main Dashboard
@app.route('/patient/dashboard')
def patient_dashboard():
    """Patient dashboard"""

    if session.get('user_type') != 'patient':
        flash('Please login to access patient dashboard', 'error')
        return redirect(url_for('patient_login'))

    return render_template('patient/dashboard.html')

#F9 Appointments View
@app.route('/patient/appointments')
def patient_appointments():
    """View patient appointments"""

    if session.get('user_type') != 'patient':
        flash('Please login to view appointments', 'error')
        return redirect(url_for('patient_login'))

    appointments = Appointment.get_by_patient(mysql, session.get('user_id'))
    return render_template('patient/appointments.html', appointments=appointments)

#F9 Medical Records View
@app.route('/patient/medical-records')
def patient_medical_records():
    """View patient medical records"""

    if session.get('user_type') != 'patient':
        flash('Please login to view medical records', 'error')
        return redirect(url_for('patient_login'))

    records = MedicalRecord.get_by_patient(mysql, session.get('user_id'))
    return render_template('patient/medical_records.html', records=records)

#F9 Appointments Cancel
@app.route('/patient/appointment/<int:appointment_id>/cancel', methods=['POST'])
def patient_cancel_appointment(appointment_id):
    """Cancel patient appointment"""

    if session.get('user_type') != 'patient':
        flash('Please login to cancel appointments', 'error')
        return redirect(url_for('patient_login'))

    try:
        # Verify appointment belongs to patient
        appointment = Appointment.find_by_id(mysql, appointment_id)
        if not appointment or appointment['patient_id'] != session.get('user_id'):
            flash('Appointment not found or access denied', 'error')
            return redirect(url_for('patient_appointments'))

        # Check if appointment is already cancelled or completed
        if appointment['status'] != 'Scheduled':
            flash('Only scheduled appointments can be cancelled', 'error')
            return redirect(url_for('patient_appointments'))

        Appointment.update_status(mysql, appointment_id, 'Cancelled')
        flash('Appointment cancelled successfully', 'success')
    except Exception as e:
        flash('Failed to cancel appointment', 'error')
        print(f"Error cancelling appointment: {e}")
        return redirect(url_for('patient_appointments'))

    return redirect(url_for('patient_appointments'))
