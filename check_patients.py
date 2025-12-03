import pymysql
pymysql.install_as_MySQLdb()

from config import Config

try:
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        db=Config.MYSQL_DB
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute('SELECT patient_id, full_name, email, phone FROM patients WHERE is_active = TRUE LIMIT 5')
    patients = cursor.fetchall()
    
    print('\n=== Active Patients ===')
    if patients:
        for p in patients:
            print(f'ID: {p["patient_id"]} | Name: {p["full_name"]} | Email: {p["email"]} | Phone: {p["phone"]}')
    else:
        print('No patients found in database')
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'Error: {e}')
