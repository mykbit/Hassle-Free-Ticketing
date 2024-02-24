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
#   Parameters:
#           eventID: ID for event. 
#           organiserID: ID of the person who created the event. (If our system allows for multiple users)
#           eventName: Name of event.
#           eventDate: Date range when event should be active
#           availableTickets: Number of tickets for event (default - 0)
def insertEvent(eventID, organiserID, eventLink, eventName, eventDate, availableTickets=0):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Insert a new event into the "events" table
    databaseCursor.execute(
        "INSERT INTO events (eventID, organiserID, eventLink, eventName, eventDate, availableTickets) VALUES (%d, %d, %s, %s, %s, %s)", 
        (eventID, organiserID, eventLink, eventName, eventDate, availableTickets)
    )

    # Save changes
    database.commit()
    database.close()
    return

def getEventDetails(eventID):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor(pymysql.cursors.DictCursor)  # Use a DictCursor for named columns

    # Query the database for event details
    databaseCursor.execute(
        "SELECT * FROM events WHERE eventID = %s",
        (eventID,)
    )

    event = databaseCursor.fetchone()

    # Close the database connection
    database.close()
    return event






#   Insert User into Database
#   Parameters:
#           name: Name of user. 
#           email: Email of User. 
#           revolutTag: revolut tag
#           payment_status: status of payment
#           events: event registered to. 
def insertUser(name, email, revolutTag, payment_status, events):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Insert a new event into the "events" table
    databaseCursor.execute(
        "INSERT INTO users (name, email, revolutTag, payment_status, event) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, email, revolutTag, payment_status, events)
    )

    # Save changes
    database.commit()
    database.close()
    return

def get_user_details(userID):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor(pymysql.cursors.DictCursor)  # Use a DictCursor for named columns

    # Query the database for user details
    databaseCursor.execute(
        "SELECT * FROM users WHERE userID = %s",
        (userID,)
    )

    user = databaseCursor.fetchone()
    # Close the database connection
    database.close()
    return user

def updateUserName(userID, updatedName):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Update the name of the user in the "users" table
    databaseCursor.execute(
        "UPDATE users SET name = %s WHERE userID = %d",
        (updatedName, userID)
    )

    # Save changes
    database.commit()
    database.close()
    return
    
#   Insert Registration
#   Parameters:
#           registrationID: registrationID
#           userID: userID
#           eventID : eventID
#           registrationDate: date registered to event. 
#           paymentStatus: status of payment 
def insertRegistration(registrationID, user, eventID, registrationDate, paymentStatus):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Insert a new event into the "events" table
    databaseCursor.execute(
        "INSERT INTO registrations (registrationID, userID, eventID, registrationDate, paymentStatus) VALUES (%d, %s, %d, %s, %s, %s)",
        (registrationID, user, eventID, registrationDate, paymentStatus)
    )

    # Save changes
    database.commit()
    database.close()
    return

def getRegistrationDetails(regID):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor(pymysql.cursors.DictCursor)  # Use a DictCursor for named columns

    # Query the database for registration details
    databaseCursor.execute(
        "SELECT * FROM registrations WHERE registrationID = %s",
        (regID,)
    )

    registration = databaseCursor.fetchone()
    # Close the database connection
    database.close()
    return registration

def updateUser(userID, name, email, revolutTag, payment_status):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Update user information in the "users" table
    databaseCursor.execute(
        "UPDATE users SET name = %s, email = %s, revolutTag = %s, payment_status = %s WHERE userID = %d",
        (name, email, revolutTag, payment_status, userID)
    )

    # Save changes
    database.commit()
    database.close()
    return