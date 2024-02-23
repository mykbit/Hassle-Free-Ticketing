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
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
    )

    cursor = conn.cursor()

    return cursor


#   Insert Event into Database
def insert(event_name, event_date, payment_address):
    # Access DB
    databaseCursor = init_db()

    # Insert a new event into the "events" table
    databaseCursor.execute(
        "INSERT INTO events (event_name, event_date, payment_link) VALUES (%s, %S, %s)", 
        (event_name, event_date, payment_address)
    )

    # Insert into Database then close. 
    databaseCursor.commit()
    databaseCursor.close()
    return


#   Insert User into Databse
def insert(name, email, revolut_tag, payment_status, event):
    databaseCursor = init_db()

    databaseCursor.execute(
        "INSERT INTO users (name, email, revolut_tag, payment_status, event) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, email, revolut_tag, payment_status, event)
    )

    databaseCursor.commit()
    databaseCursor.close()
    return

    

