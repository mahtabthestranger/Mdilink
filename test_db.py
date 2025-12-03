import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv('MYSQL_HOST', 'localhost')
user = os.getenv('MYSQL_USER', 'root')
password = os.getenv('MYSQL_PASSWORD', '')
db = os.getenv('MYSQL_DB', 'medilink_db')

print(f"Attempting to connect to {host} as {user}...")

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Connection successful!")
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print(f"Database version: {result}")
        
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")
