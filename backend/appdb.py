from flask import Flask, request, jsonify, send_from_directory
import os
import psycopg2
import logging
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up PostgreSQL connection using environment variables
DATABASE_URL = (
    f"dbname='{os.getenv('DB_NAME', 'mydb')}' "
    f"user='{os.getenv('DB_USER', 'myuser')}' "
    f"password='{os.getenv('DB_PASSWORD', 'Rajats008@')}' "
    f"host='{os.getenv('DB_HOST', '34.69.63.44')}'"
)

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        logger.info("Connected to PostgreSQL database")
        return conn
    except Exception as e:
        logger.error(f"An error occurred while connecting to the database: {e}")
        raise Exception(f"An error occurred while connecting to the database: {e}")

def create_table():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL
        );
        '''
        cursor.execute(create_table_query)
        conn.commit()
        logger.info("Table 'students' created successfully or already exists.")
    except Exception as e:
        logger.error(f"An error occurred while creating the table: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Handle form submission and insert student information into the database
#@app.route('/')
#def index():
 #   return send_from_directory('../frontend', 'index.html')
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('name')
    student_id = data.get('id')
    course = data.get('course')
    
    if not name or not student_id or not course:
        return jsonify({'error': 'Missing required fields'})

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = "INSERT INTO students (name, student_id, course) VALUES (%s, %s, %s);"
        cursor.execute(insert_query, (name, student_id, course))
        conn.commit()
        logger.info("Student information inserted into the database")
        return jsonify({'message': 'Student information inserted successfully', 'name': name, 'id': student_id, 'course': course})
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"An error occurred while inserting student information into the database: {e}")
        return jsonify({'error': 'An error occurred while inserting student information into the database'})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    # Create the table when the application starts
    create_table()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
