# Medilink Hospital Management System

A comprehensive hospital management system built with Flask and MySQL.

## 🏥 Project Overview

This system manages hospital operations including:
- Admin management of doctors and patients
- Doctor appointment scheduling and medical records
- Patient registration, appointment booking, and medical history

## 👥 Team Members & Features

### Mahtab - Patient Authentication (F6, F7)
**Branch:** `feature/mahtab-patient-auth`

**Features:**
- **F6: Patient Registration** - Self-registration system for new patients
- **F7: Patient Login** - Secure login for registered patients

**Documentation:** [docs/Mahtab_features.md](docs/Mahtab_features.md)

---

### Al Mamun Oualid - Doctor Features (F3, F4, F5)
**Branch:** `feature/oualid-doctor-features`

**Features:**
- **F3: Doctor Login** - Secure login with doctor ID and password
- **F4: Doctor View Appointments** - View and manage scheduled appointments
- **F5: Doctor Medical Records** - Add and update patient medical records

**Documentation:** [docs/Oualid_features.md](docs/Oualid_features.md)

---

### Prottoy - Admin Features (F1, F2)
**Branch:** `feature/prottoy-admin-features`

**Features:**
- **F1: Admin Login** - Secure admin authentication
- **F2: Admin Manage Doctors** - Add, edit, and delete doctor profiles

**Documentation:** [docs/Prottoy_features.md](docs/Prottoy_features.md)

---

### Mahieer Haai - Patient Features (F8, F9)
**Branch:** `feature/mahieer-patient-features`

**Features:**
- **F8: Patient Book Appointment** - Book appointments with available doctors
- **F9: Patient View Medical History** - View past appointments and medical records

**Documentation:** [docs/Mahieer_features.md](docs/Mahieer_features.md)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/medilink-hospital.git
cd medilink-hospital
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up database:**
```bash
# Create database in MySQL
mysql -u root -p
CREATE DATABASE medilink_db;
exit;

# Run database setup script
python database/setup_database.py
```

4. **Configure environment:**
```bash
# Copy .env.example to .env and update with your database credentials
# (Note: .env is gitignored for security)
```

5. **Run the application:**
```bash
python app.py
```

6. **Access the application:**
- Open browser: `http://localhost:5000`

---

## 📁 Project Structure

```
medilink4/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .gitignore            # Git ignore rules
│
├── models/               # Database models
│   ├── admin.py
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   └── medical_record.py
│
├── templates/            # HTML templates
│   ├── admin/           # Admin pages
│   ├── doctor/          # Doctor pages
│   └── patient/         # Patient pages
│
├── static/              # CSS, JS, images
│   ├── css/
│   └── js/
│
├── tests/               # Test files
│   ├── test_auth.py
│   └── test_appointments.py
│
├── docs/                # Documentation
│   ├── Mahtab_features.md
│   ├── Oualid_features.md
│   ├── Prottoy_features.md
│   └── Mahieer_features.md
│
└── database/            # Database scripts
    └── setup_database.py
```

---

## 🔐 User Roles & Access

### Admin
- **Login:** Username and password
- **Access:** Full system control
- **Features:** Manage doctors, view all patients, system statistics

### Doctor
- **Login:** Doctor ID and password (provided by admin)
- **Access:** Patient records and appointments
- **Features:** View appointments, add/edit medical records

### Patient
- **Login:** Email and password (self-registered)
- **Access:** Personal dashboard
- **Features:** Book appointments, view medical history

---

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Feature Tests
```bash
# Mahtab's features
python -m pytest tests/test_Mahtab_features.py -v

# Oualid's features
python -m pytest tests/test_Oualid_features.py -v

# Prottoy's features
python -m pytest tests/test_Prottoy_features.py -v

# Mahieer's features
python -m pytest tests/test_Mahieer_features.py -v
```

### Manual Testing
1. Start the application: `python app.py`
2. Follow test cases in respective feature documentation
3. Verify database changes using MySQL Workbench

---

## 🌿 Git Workflow

### For Team Members

1. **Clone and setup:**
```bash
git clone https://github.com/YOUR_USERNAME/medilink-hospital.git
cd medilink-hospital
```

2. **Create your feature branch:**
```bash
# Use the setup script (Windows)
setup_member.bat

# Or manually:
git checkout -b feature/your-name-features
```

3. **Make changes and commit:**
```bash
git add .
git commit -m "Add documentation for F6 and F7"
```

4. **Push to GitHub:**
```bash
git push -u origin feature/your-name-features
```

5. **Create Pull Request:**
- Go to GitHub repository
- Click "Pull Requests" → "New Pull Request"
- Select your branch and create PR

---

## 📊 Database Schema

### Tables
- `admins` - Admin user accounts
- `doctors` - Doctor profiles and credentials
- `patients` - Patient information
- `appointments` - Appointment bookings
- `medical_records` - Patient medical history

### Relationships
- Appointments link patients and doctors
- Medical records link patients and doctors
- Admins manage doctors

---

## 🛠️ Technologies Used

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Flask-Session with password hashing
- **ORM:** Flask-MySQLdb

---

## 📝 Feature Requirements

### F1: Admin Login ✅
- Secure authentication with username/password
- Redirect to dashboard on success
- Error handling for invalid credentials

### F2: Admin Manage Doctors ✅
- Add new doctors with all required fields
- Edit existing doctor information
- Delete/deactivate doctor accounts
- Validation and confirmation messages

### F3: Doctor Login ✅
- Authentication with doctor ID and password
- Account status verification
- Error handling for invalid/inactive accounts

### F4: Doctor View Appointments ✅
- Display all scheduled appointments
- Filter by date and patient name
- Show appointment details

### F5: Doctor Medical Records ✅
- Add new medical records with diagnosis
- Update existing records
- Required field validation

### F6: Patient Registration ✅
- Self-registration form
- Duplicate email detection
- Password validation
- Immediate login after registration

### F7: Patient Login ✅
- Email and password authentication
- Error handling for invalid credentials
- User not found detection

### F8: Patient Book Appointment ✅
- Select doctor and time slot
- Availability checking
- Booking confirmation
- Error handling for unavailable slots

### F9: Patient View Medical History ✅
- Display past appointments
- Show medical records with diagnosis
- Filter and search capabilities

---

## 🐛 Known Issues

[Team members: Add any known issues here]

---

## 🔮 Future Enhancements

- Email notifications for appointments
- SMS reminders
- Online payment integration
- Prescription printing
- Medical report generation
- Mobile app

---

## 📞 Support

For issues or questions:
- Check feature documentation in `docs/` folder
- Review test cases in `tests/` folder
- Contact team members via [communication channel]

---

## 📄 License

[Your License Here]

---

## 🙏 Acknowledgments

- Course Professor: [Professor Name]
- Team Members: Mahtab, Al Mamun Oualid, Prottoy, Mahieer Haai
- Institution: [Your University]

---

**Last Updated:** December 2025  
**Version:** 1.0.0
