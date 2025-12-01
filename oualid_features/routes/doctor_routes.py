def doctor_medical_records_route(app, mysql, Patient, MedicalRecord):
    
    @app.route('/doctor/patients')
    def doctor_patients():
        if session.get('user_type') != 'doctor':
            flash('Please login to access doctor dashboard', 'error')
            return redirect(url_for('doctor_login'))
        
        patients = Patient.get_all(mysql)
        return render_template('doctor/patients.html', patients=patients)
    
    
    @app.route('/doctor/patient/<int:patient_id>')
    def doctor_view_patient(patient_id):
        if session.get('user_type') != 'doctor':
            flash('Please login to access doctor dashboard', 'error')
            return redirect(url_for('doctor_login'))
        
        patient = Patient.find_by_id(mysql, patient_id)
        if not patient:
            flash('Patient not found', 'error')
            return redirect(url_for('doctor_patients'))
        
        records = MedicalRecord.get_by_patient(mysql, patient_id)
        
        return render_template(
            'doctor/patient_details.html', 
            patient=patient, 
            records=records
        )
    
    
    @app.route('/doctor/patient/<int:patient_id>/add-record', methods=['GET', 'POST'])
    def doctor_add_record(patient_id):
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
                flash('Please enter mandatory details', 'error')
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
                
                flash('Record saved successfully', 'success')
                return redirect(url_for('doctor_view_patient', patient_id=patient_id))
                
            except Exception as e:
                flash('Failed to add medical record', 'error')
                print(f"Error adding record: {e}")
                return redirect(url_for('doctor_add_record', patient_id=patient_id))
        
        return render_template('doctor/add_record.html', patient=patient)
    
    
    @app.route('/doctor/record/<int:record_id>/edit', methods=['GET', 'POST'])
    def doctor_edit_record(record_id):
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
                flash('Please enter mandatory details', 'error')
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
