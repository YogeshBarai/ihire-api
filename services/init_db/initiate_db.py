# ----------------------------------------------------------------------------------
# Usage:
# This script is used to configure tables on the dataabase
# # ----------------------------------------------------------------------------------
# # Pre requisites:
# # Database connection string, database name, userid & password are to be configured 
# #   as system environment variables 
# # These values are fetched from the environment variables
# # ----------------------------------------------------------------------------------
# # Revision history:
# ## Date           Author          Comment
# ## 20230618       Yogesh B        Initial version
# # ----------------------------------------------------------------------------------

# # ToDo: Defining FK constraints later

# Import all libraries
# Import the necessary libraries
from flask import Blueprint
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create a Flask blueprint for the database-related functionality
db_blueprint = Blueprint('InitiateDatabase', __name__)

# Database connection parameters
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


# @db_blueprint.record_once
def create_database():
    try:
        # Connect to the database
        with connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
        ) as connection:
            # Create a cursor object
            cursor = connection.cursor()

            # Create the Candidates table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Candidates (
                    candidate_id INT PRIMARY KEY AUTO_INCREMENT,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    address VARCHAR(100),
                    resume_file_path VARCHAR(100)
                )
                """
            )

            # Create the JobPostings table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS JobPostings (
                    job_id INT PRIMARY KEY AUTO_INCREMENT,
                    job_title VARCHAR(100),
                    company_name VARCHAR(100),
                    location VARCHAR(100),
                    description TEXT,
                    requirements TEXT,
                    posted_date DATETIME
                )
                """
            )

            # Create the Company table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Company (
                    company_id INT PRIMARY KEY AUTO_INCREMENT,
                    company_name VARCHAR(100),
                    address VARCHAR(200), 
                    city VARCHAR(100),
                    state VARCHAR(100),
                    on_boarding_date DATETIME,
                    company_poc_name VARCHAR(100),
                    company_poc_contact VARCHAR(20),
                    company_poc_email VARCHAR(100)
                )
                """
            )

            # Commit the changes
            connection.commit()

            print('Database created successfully')
    except Error as e:
        print(f'Error creating database: {e}')


@db_blueprint.route('/api/create_database', methods=['POST'])
def trigger_create_database():
    create_database()
    return 'Database created successfully'
