# Medilink Hospital Management System

A comprehensive web-based Patient Appointment and Record Management System built with Flask, MySQL, and Tailwind CSS.

## Features

### Admin Features
- Secure login system
- Add, edit, and delete doctor profiles
- Manage appointments
- View all system data

### Doctor Features
- Secure login with doctor ID
- View upcoming appointments
- Add and update patient medical records
- Filter appointments by date/patient

### Patient Features
- Online registration
- Secure login
- Book appointments with doctors
- View appointment history
- Access medical records

## Technology Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, Tailwind CSS
- **Architecture**: MVC (Model-View-Controller)

## Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   cd medilink4
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update MySQL credentials in `.env`:
     ```
     MYSQL_HOST=localhost
     MYSQL_USER=root
     MYSQL_PASSWORD=your_password
     MYSQL_DB=medilink_db
     ```

4. **Initialize the database**
   ```bash
   python database/init_db.py
   ```
   
   This will:
   - Create the `medilink_db` database
   - Create all necessary tables

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and go to: `http://localhost:5000`

## Initial Setup

After running the database initialization, you must create your first admin account manually through the database or via an admin creation endpoint. No default credentials are provided for security reasons.

## Database Schema

### Tables
- `admins` - Administrator accounts
- `doctors` - Doctor profiles and credentials
- `patients` - Patient information
- `appointments` - Appointment bookings
- `medical_records` - Patient medical history

## Project Structure

```
medilink4/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── models/               # Database models (M)
│   ├── admin.py
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   └── medical_record.py
├── controllers/          # Business logic (C)
├── templates/            # HTML templates (V)
│   ├── base.html
│   ├── index.html
│   ├── admin/
│   ├── doctor/
│   └── patient/
└── database/
    └── init_db.py        # Database initialization
```

## Development

To run in development mode:
```bash
set FLASK_ENV=development  # Windows
export FLASK_ENV=development  # Linux/Mac
python app.py
```

## License

This project is for educational purposes.

## Support

For issues or questions, please contact the development team.
