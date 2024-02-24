import pymysql
import os

# Used to test the connection to the database from local environment, which allows bypass of Github Secrets
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def init_db():
    # Retrieve database credentials from the environment
    db_host = os.environ.get('DATABASE_HOST')
    db_port = os.environ.get('DATABASE_PORT')
    db_user = os.environ.get('DATABASE_USER')
    db_password = os.environ.get('DATABASE_PASSWORD')
    db_name = os.environ.get('DATABASE_NAME')

    # Establish a connection to the MySQL database
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='your_test_user',
        password='your_password',
        database='your_test_database',
    )

    return conn


#   Insert Event into Database
def insert(event_name, event_date, payment_address):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Insert a new event into the "events" table
    databaseCursor.execute(
        "INSERT INTO events (event_name, event_date, payment_link) VALUES (%s, %s, %s)", 
        (event_name, event_date, payment_address)
    )

    # Save changes
    database.commit()
    database.close()
    return


#   Insert User into Databse
def inserts(name, email, revolut_tag, payment_status, event):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Insert a new event into the "events" table
    databaseCursor.execute(
        "INSERT INTO users (name, email, revolut_tag, payment_status, event) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, email, revolut_tag, payment_status, event)
    )

    # Save changes
    database.commit()
    database.close()
    return

    

