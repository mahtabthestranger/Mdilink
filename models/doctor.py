"""
Doctor Model
============

Handles all database operations related to doctors including authentication,
creation, retrieval, and management of doctor accounts.

Author: Al Mamun Oualid
Feature: F3 (Doctor Login), F4 (View Appointments), F5 (Medical Records)
"""

from werkzeug.security import generate_password_hash, check_password_hash

class Doctor:
    """
    Doctor model class for managing doctor accounts and authentication.
    
    This class provides static methods for CRUD operations on doctor records
    and handles password hashing for secure authentication.
    
    Attributes:
        None (all methods are static)
    
    Example:
        >>> doctor = Doctor.verify_password(mysql, 'DOC001', 'password123')
        >>> if doctor:
        ...     print(f"Welcome, Dr. {doctor['full_name']}")
    """
    
    @staticmethod
    def create(mysql, doctor_code, password, full_name, university, email, phone, 
               specialization=None, qualification=None, address=None, created_by=None):
        """
        Create a new doctor account with hashed password.
        
        Args:
            mysql: MySQL database connection object
            doctor_code (str): Unique identifier for the doctor (e.g., 'DOC001')
            password (str): Plain text password (will be hashed)
            full_name (str): Doctor's full name
            university (str): Medical university/institution
            email (str): Doctor's email address
            phone (str): Doctor's phone number
            specialization (str, optional): Medical specialization. Defaults to None.
            qualification (str, optional): Medical qualifications. Defaults to None.
            address (str, optional): Doctor's address. Defaults to None.
            created_by (int, optional): Admin ID who created this account. Defaults to None.
        
        Returns:
            int: The ID of the newly created doctor
        
        Raises:
            Exception: If database operation fails
        
        Example:
            >>> doctor_id = Doctor.create(
            ...     mysql=mysql,
            ...     doctor_code='DOC001',
            ...     password='secure_password',
            ...     full_name='Dr. John Smith',
            ...     university='Harvard Medical School',
            ...     email='john@hospital.com',
            ...     phone='1234567890'
            ... )
        
        Note:
            Password is automatically hashed using PBKDF2-SHA256 before storage.
        """
        cursor = mysql.connection.cursor()
        hashed_password = generate_password_hash(password)
        
        cursor.execute("""
            INSERT INTO doctors (doctor_code, password, full_name, university, specialization,
                               qualification, email, phone, address, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (doctor_code, hashed_password, full_name, university, specialization,
              qualification, email, phone, address, created_by))
        
        mysql.connection.commit()
        doctor_id = cursor.lastrowid
        cursor.close()
        return doctor_id
    
    @staticmethod
    def find_by_code(mysql, doctor_code):
        """
        Find an active doctor by their unique doctor code.
        
        Args:
            mysql: MySQL database connection object
            doctor_code (str): Unique doctor identifier
        
        Returns:
            dict: Doctor record if found and active, None otherwise
        
        Example:
            >>> doctor = Doctor.find_by_code(mysql, 'DOC001')
            >>> if doctor:
            ...     print(doctor['full_name'])
        
        Note:
            Only returns active doctors (is_active = TRUE)
        """
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM doctors WHERE doctor_code = %s AND is_active = TRUE", (doctor_code,))
        doctor = cursor.fetchone()
        cursor.close()
        return doctor
    
    @staticmethod
    def find_by_id(mysql, doctor_id):
        """
        Find a doctor by their database ID.
        
        Args:
            mysql: MySQL database connection object
            doctor_id (int): Doctor's database ID
        
        Returns:
            dict: Doctor record if found, None otherwise
        
        Example:
            >>> doctor = Doctor.find_by_id(mysql, 1)
            >>> print(doctor['doctor_code'])
        """
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
        doctor = cursor.fetchone()
        cursor.close()
        return doctor
    
    @staticmethod
    def get_all(mysql, active_only=True):
        """
        Retrieve all doctors from the database.
        
        Args:
            mysql: MySQL database connection object
            active_only (bool, optional): If True, only return active doctors.
                                         Defaults to True.
        
        Returns:
            list: List of doctor records ordered by full name
        
        Example:
            >>> all_doctors = Doctor.get_all(mysql)
            >>> active_doctors = Doctor.get_all(mysql, active_only=True)
            >>> for doctor in all_doctors:
            ...     print(doctor['full_name'])
        """
        cursor = mysql.connection.cursor()
        if active_only:
            cursor.execute("SELECT * FROM doctors WHERE is_active = TRUE ORDER BY full_name")
        else:
            cursor.execute("SELECT * FROM doctors ORDER BY full_name")
        doctors = cursor.fetchall()
        cursor.close()
        return doctors
    
    @staticmethod
    def verify_password(mysql, doctor_code, password):
        """
        Verify doctor login credentials (F3: Doctor Login).
        
        This method is used for doctor authentication. It finds the doctor
        by code and verifies the password using secure hashing.
        
        Args:
            mysql: MySQL database connection object
            doctor_code (str): Doctor's unique code
            password (str): Plain text password to verify
        
        Returns:
            dict: Doctor record if credentials are valid, None otherwise
        
        Example:
            >>> doctor = Doctor.verify_password(mysql, 'DOC001', 'password123')
            >>> if doctor:
            ...     session['user_id'] = doctor['doctor_id']
            ...     print("Login successful")
            >>> else:
            ...     print("Invalid credentials")
        
        Note:
            - Only active doctors can log in
            - Password is verified using check_password_hash
            - Used in F3: Doctor Login feature
        """
        doctor = Doctor.find_by_code(mysql, doctor_code)
        if doctor and check_password_hash(doctor['password'], password):
            return doctor
        return None
    
    @staticmethod
    def update(mysql, doctor_id, **kwargs):
        """
        Update doctor information.
        
        Args:
            mysql: MySQL database connection object
            doctor_id (int): ID of the doctor to update
            **kwargs: Field-value pairs to update
        
        Returns:
            bool: True if update successful
        
        Example:
            >>> Doctor.update(
            ...     mysql,
            ...     doctor_id=1,
            ...     full_name='Dr. John Smith Jr.',
            ...     email='newmail@hospital.com'
            ... )
        
        Note:
            If 'password' is in kwargs, it will be automatically hashed
        """
        cursor = mysql.connection.cursor()
        
        fields = []
        values = []
        for key, value in kwargs.items():
            if key == 'password':
                value = generate_password_hash(value)
            fields.append(f"{key} = %s")
            values.append(value)
        
        values.append(doctor_id)
        query = f"UPDATE doctors SET {', '.join(fields)} WHERE doctor_id = %s"
        
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return True
    
    @staticmethod
    def delete(mysql, doctor_id):
        """
        Soft delete a doctor account by setting is_active to FALSE.
        
        This method does not permanently delete the doctor record,
        allowing for data retention and potential account recovery.
        
        Args:
            mysql: MySQL database connection object
            doctor_id (int): ID of the doctor to deactivate
        
        Returns:
            bool: True if deactivation successful
        
        Example:
            >>> Doctor.delete(mysql, doctor_id=1)
            >>> # Doctor account is now inactive but data is preserved
        
        Note:
            Inactive doctors cannot log in to the system
        """
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE doctors SET is_active = FALSE WHERE doctor_id = %s", (doctor_id,))
        mysql.connection.commit()
        cursor.close()
        return True
    
    @staticmethod
    def get_by_university(mysql, university):
        """
        Get all active doctors from a specific university.
        
        Args:
            mysql: MySQL database connection object
            university (str): Name of the medical university
        
        Returns:
            list: List of doctor records from the specified university
        
        Example:
            >>> doctors = Doctor.get_by_university(mysql, 'Harvard Medical School')
            >>> for doctor in doctors:
            ...     print(f"{doctor['full_name']} - {doctor['specialization']}")
        """
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT * FROM doctors 
            WHERE university = %s AND is_active = TRUE 
            ORDER BY full_name
        """, (university,))
        doctors = cursor.fetchall()
        cursor.close()
        return doctors
