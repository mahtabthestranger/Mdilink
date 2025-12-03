================================================================================
Code Examples - Admin Integration
================================================================================

Code Examples for Common Tasks
===============================

This section provides practical code examples for integrating with the
Medilink admin API.

Python Examples
===============

Admin Login (Python)
--------------------

**Login and retrieve session**

.. code-block:: python

    import requests
    from requests.auth import HTTPBasicAuth

    session = requests.Session()

    login_response = session.post(
        'http://localhost:5000/admin/login',
        data={
            'username': 'admin',
            'password': 'password123'
        }
    )

    if login_response.status_code == 200:
        print("Login successful!")
    else:
        print("Login failed")

List Doctors (Python)
---------------------

**Retrieve list of doctors**

.. code-block:: python

    import requests

    session = requests.Session()

    session.post(
        'http://localhost:5000/admin/login',
        data={'username': 'admin', 'password': 'password123'}
    )

    response = session.get(
        'http://localhost:5000/admin/doctors',
        params={
            'search': 'cardio',
            'page': 1
        }
    )

    print(response.status_code)
    print(response.text[:500]) 

Add Doctor (Python)
-------------------

**Create new doctor**

.. code-block:: python

    import requests

    session = requests.Session()

    session.post(
        'http://localhost:5000/admin/login',
        data={'username': 'admin', 'password': 'password123'}
    )

    doctor_data = {
        'full_name': 'Dr. Sarah Johnson',
        'specialty': 'Cardiology',
        'phone': '555-0123',
        'email': 'sarah.johnson@medilink.com',
        'experience': 8,
        'license_number': 'MD123456',
        'password': 'SecurePassword123'
    }

    response = session.post(
        'http://localhost:5000/admin/doctors/add',
        data=doctor_data
    )

    if response.url.endswith('/admin/doctors'):
        print("Doctor added successfully!")
    else:
        print("Error adding doctor")
        print(response.text)

Edit Patient (Python)
---------------------

**Update patient information**

.. code-block:: python

    import requests

    session = requests.Session()

    session.post(
        'http://localhost:5000/admin/login',
        data={'username': 'admin', 'password': 'password123'}
    )

    patient_id = 42
    patient_data = {
        'full_name': 'John Anderson',
        'email': 'john.a@email.com',
        'phone': '555-4321',
        'date_of_birth': '1985-03-15',
        'gender': 'M',
        'address': '456 Oak Ave',
        'city': 'Portland',
        'state': 'OR',
        'postal_code': '97201'
    }

    response = session.post(
        f'http://localhost:5000/admin/patients/edit/{patient_id}',
        data=patient_data
    )

    if response.url.endswith('/admin/patients'):
        print("Patient updated successfully!")

Delete Doctor (Python)
----------------------

**Delete a doctor**

.. code-block:: python

    import requests

    session = requests.Session()

    session.post(
        'http://localhost:5000/admin/login',
        data={'username': 'admin', 'password': 'password123'}
    )

    doctor_id = 5
    response = session.post(
        f'http://localhost:5000/admin/doctors/delete/{doctor_id}',
        data={'confirm': 'yes'}
    )

    print("Doctor deleted successfully!" if response.ok else "Error")

JavaScript Examples
====================

Admin Login (JavaScript)
------------------------

**Authenticate and get session**

.. code-block:: javascript

    async function adminLogin() {
        const formData = new FormData();
        formData.append('username', 'admin');
        formData.append('password', 'password123');

        const response = await fetch('/admin/login', {
            method: 'POST',
            body: formData,
            credentials: 'include'  
        });

        if (response.redirected) {
            console.log('Login successful, redirected to:', response.url);
            return true;
        } else {
            console.log('Login failed');
            return false;
        }
    }

    adminLogin();

Fetch Doctors List (JavaScript)
--------------------------------

**Get list of doctors from admin panel**

.. code-block:: javascript

    async function getDoctorsList() {
        const response = await fetch(
            '/admin/doctors?search=cardio&page=1',
            {
                method: 'GET',
                credentials: 'include'
            }
        );

        if (response.ok) {
            const html = await response.text();
            document.getElementById('content').innerHTML = html;
        } else if (response.status === 302) {
            window.location.href = '/admin/login';
        }
    }

    getDoctorsList();

Add Doctor (JavaScript)
-----------------------

**Create new doctor from form**

.. code-block:: javascript

    async function addDoctor() {
        const doctorData = {
            full_name: 'Dr. Michael Chen',
            specialty: 'Orthopedics',
            phone: '555-7890',
            email: 'michael.chen@medilink.com',
            experience: 12,
            license_number: 'MD987654',
            password: 'SecurePassword123'
        };

        const formData = new FormData();
        Object.keys(doctorData).forEach(key => {
            formData.append(key, doctorData[key]);
        });

        const response = await fetch('/admin/doctors/add', {
            method: 'POST',
            body: formData,
            credentials: 'include'
        });

        if (response.redirected) {
            console.log('Doctor added, redirecting to:', response.url);
            window.location.href = response.url;
        } else {
            console.log('Failed to add doctor');
            const html = await response.text();
            document.getElementById('form-container').innerHTML = html;
        }
    }

Edit Patient (JavaScript)
--------------------------

**Update patient information**

.. code-block:: javascript

    async function updatePatient(patientId, patientData) {
        const formData = new FormData();
        
        Object.keys(patientData).forEach(key => {
            formData.append(key, patientData[key]);
        });

        const response = await fetch(
            `/admin/patients/edit/${patientId}`,
            {
                method: 'POST',
                body: formData,
                credentials: 'include'
            }
        );

        if (response.redirected) {
            alert('Patient updated successfully!');
            window.location.href = '/admin/patients';
        } else {
            alert('Error updating patient');
        }
    }

    updatePatient(42, {
        full_name: 'Jane Doe',
        email: 'jane.doe@email.com',
        phone: '555-1234',
        gender: 'F',
        date_of_birth: '1990-05-20'
    });

Delete Patient (JavaScript)
----------------------------

**Remove a patient**

.. code-block:: javascript

    async function deletePatient(patientId) {
        if (!confirm('Are you sure you want to delete this patient?')) {
            return;
        }

        const formData = new FormData();
        formData.append('confirm', 'yes');

        const response = await fetch(
            `/admin/patients/delete/${patientId}`,
            {
                method: 'POST',
                body: formData,
                credentials: 'include'
            }
        );

        if (response.redirected) {
            console.log('Patient deleted successfully');
            window.location.href = '/admin/patients';
        }
    }

cURL Examples
=============

Login (cURL)
------------

**Authenticate and save session**

.. code-block:: bash

    curl -c cookies.txt -X POST http://localhost:5000/admin/login \
         -d "username=admin&password=password123"

List Doctors (cURL)
-------------------

**Retrieve doctors list**

.. code-block:: bash

    curl -b cookies.txt \
         "http://localhost:5000/admin/doctors?search=cardio&page=1" \
         -o doctors.html

Add Doctor (cURL)
-----------------

**Create new doctor**

.. code-block:: bash

    curl -b cookies.txt -X POST http://localhost:5000/admin/doctors/add \
         -d "full_name=Dr.%20Robert%20Wilson" \
         -d "specialty=Pediatrics" \
         -d "phone=555-5555" \
         -d "email=robert.wilson@medilink.com" \
         -d "experience=15" \
         -d "license_number=MD555555" \
         -d "password=SecurePass123"

Edit Patient (cURL)
-------------------

**Update patient details**

.. code-block:: bash

    curl -b cookies.txt -X POST http://localhost:5000/admin/patients/edit/42 \
         -d "full_name=Jane%20Smith" \
         -d "email=jane.smith@email.com" \
         -d "phone=555-9999" \
         -d "gender=F" \
         -d "date_of_birth=1988-07-10"

Delete Doctor (cURL)
--------------------

**Remove a doctor**

.. code-block:: bash

    curl -b cookies.txt -X POST http://localhost:5000/admin/doctors/delete/5 \
         -d "confirm=yes"

Practical Workflows
===================

Complete Admin Session Workflow
--------------------------------

**Python workflow: Login → View Stats → Add Doctor → List**

.. code-block:: python

    import requests
    from bs4 import BeautifulSoup

    session = requests.Session()

    session.post('http://localhost:5000/admin/login', data={
        'username': 'admin',
        'password': 'password123'
    })
    print("✓ Logged in")

    dashboard = session.get('http://localhost:5000/admin/dashboard')
    print("✓ Dashboard loaded")

    session.post('http://localhost:5000/admin/doctors/add', data={
        'full_name': 'Dr. New Doctor',
        'specialty': 'Surgery',
        'phone': '555-0000',
        'email': 'new.doctor@medilink.com',
        'experience': 5,
        'license_number': 'MD000000',
        'password': 'TempPassword123'
    })
    print("✓ Doctor added")

    response = session.get('http://localhost:5000/admin/doctors')
    print(f"✓ Retrieved doctors list")

Frontend Integration Example
-----------------------------

**HTML form that integrates with admin API**

.. code-block:: html

    <!DOCTYPE html>
    <html>
    <head>
        <title>Add Doctor</title>
    </head>
    <body>
        <form id="addDoctorForm">
            <input type="text" name="full_name" placeholder="Full Name" required>
            <select name="specialty" required>
                <option value="">Select Specialty</option>
                <option value="Cardiology">Cardiology</option>
                <option value="Neurology">Neurology</option>
                <option value="Orthopedics">Orthopedics</option>
            </select>
            <input type="tel" name="phone" placeholder="Phone" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="number" name="experience" placeholder="Years Experience">
            <input type="text" name="license_number" placeholder="License Number" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Add Doctor</button>
        </form>

        <script>
            document.getElementById('addDoctorForm').addEventListener('submit', 
                async function(e) {
                    e.preventDefault();
                    
                    const formData = new FormData(this);
                    
                    const response = await fetch('/admin/doctors/add', {
                        method: 'POST',
                        body: formData,
                        credentials: 'include'
                    });
                    
                    if (response.redirected) {
                        window.location.href = '/admin/doctors';
                    } else {
                        alert('Error adding doctor');
                    }
                }
            );
        </script>
    </body>
    </html>

Error Handling Examples
=======================

Python Error Handling
---------------------

.. code-block:: python

    import requests

    session = requests.Session()

    try:
        response = session.post(
            'http://localhost:5000/admin/login',
            data={'username': 'admin', 'password': 'wrong_password'},
            timeout=5
        )

        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to server")
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
    except Exception as e:
        print(f"Unexpected error: {e}")

JavaScript Error Handling
--------------------------

.. code-block:: javascript

    async function addDoctorWithErrorHandling() {
        try {
            const response = await fetch('/admin/doctors/add', {
                method: 'POST',
                body: formData,
                credentials: 'include'
            });

            if (!response.ok && response.status !== 302) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            if (response.redirected) {
                window.location.href = response.url;
            }

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    }

Request/Response Examples
=========================

Successful Doctor Add Request
------------------------------

**Request**

.. code-block:: bash

    POST /admin/doctors/add HTTP/1.1
    Host: localhost:5000
    Cookie: session=abc123def456...
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 156

    full_name=Dr.+Emily+Davis&specialty=Dermatology&phone=555-3210&
    email=emily.davis@medilink.com&experience=7&license_number=MD321000&
    password=SecurePass123

**Response**

.. code-block:: http

    HTTP/1.1 302 FOUND
    Location: /admin/doctors
    Set-Cookie: session=...
    Content-Length: 0

    [Flash Message: "Doctor added successfully!"]

Failed Validation Request
--------------------------

**Request (missing email)**

.. code-block:: bash

    POST /admin/doctors/add HTTP/1.1
    Host: localhost:5000
    Cookie: session=abc123def456...
    Content-Type: application/x-www-form-urlencoded

    full_name=Dr.+Test&specialty=Cardiology&phone=555-0000&
    license_number=MD000000&password=Test123456

**Response**

.. code-block:: http

    HTTP/1.1 200 OK
    Content-Type: text/html; charset=utf-8

    [Re-rendered form with error: "Please enter a valid email"]

Tips and Best Practices
=======================

Session Management
------------------

- Always use ``credentials: 'include'`` in JavaScript fetch
- Use ``requests.Session()`` in Python to maintain cookies
- Use ``-b cookies.txt`` in cURL to use saved session

Data Validation
---------------

- Validate on client side for better UX
- Always validate on server (never trust client)
- Use same validation rules on both sides

Error Handling
--------------

- Check HTTP status codes
- Handle redirects (302 = success or auth needed)
- Display user-friendly error messages
- Log errors for debugging

Security Notes
--------------

- Never log passwords
- Always use HTTPS in production
- Store API keys securely
- Validate all user input
- Use prepared statements to prevent SQL injection

Next Steps
==========

1. **Study API Reference** → See :doc:`api_endpoints`
2. **Troubleshoot Issues** → See :doc:`troubleshooting`
3. **View Endpoints** → See :doc:`doctor_management`
4. **Patient Operations** → See :doc:`patient_management`
5. **Dashboard Stats** → See :doc:`admin_dashboard`
