from flask import current_app
import jwt
import pymysql
import os
import json
import time

# Used to test the connection to the database from local environment, which allows bypass of Github Secrets
# from dotenv import load_dotenv
def connect_db():
    # Retrieve database credentials from the environment
    db_host = os.environ.get('DATABASE_HOST')
    db_port = int(os.environ.get('DATABASE_PORT'))
    db_user = os.environ.get('DATABASE_USER')
    db_password = os.environ.get('DATABASE_PASSWORD')
    db_name = os.environ.get('DATABASE_NAME')

    # Establish a connection to the MySQL database
    connection = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
    )

    return connection

def get_contents_clients():
    database = connect_db()
    databaseCursor = database.cursor()

    databaseCursor.execute("SELECT * FROM Clients")

    rows = databaseCursor.fetchall()
    database.close()
    return rows

def get_contents_sessions():
    database = connect_db()
    databaseCursor = database.cursor()

    databaseCursor.execute("SELECT * FROM Sessions")

    rows = databaseCursor.fetchall()
    database.close()
    return rows

# Client
def insertClient(name, email, password):
    
    # Access DB
    database = connect_db()
    databaseCursor = database.cursor()

    # Insert a new user into the "users" table
    databaseCursor.execute(
        "INSERT INTO Clients (email, password, name) VALUES (%s, %s, %s)",
        (email, password, name)
    )

    # Save changes
    database.commit()
    database.close()
    return True


def updateClientEmail(userID, updatedEmail):

    database = connect_db()
    databaseCursor = database.cursor()

    databaseCursor.execute(
        "UPDATE Clients SET email = %s WHERE id = %s",
        (updatedEmail, userID)
    )

    database.commit()
    database.close()
    return json.dumps({"success": True, "userID": userID, "updatedName": updatedEmail})

def updateClient(userID, name, email, password):
    database = connect_db()
    databaseCursor = database.cursor()
    databaseCursor.execute(
        "UPDATE Clients SET email = %s, password = %s, name = %s WHERE id = %s",
        (email, password, name, userID)
    )
    database.commit()
    database.close()
    return json.dumps({"success": True, "userID": userID, "updatedInfo": {"name": name, "email": email}})

def getClientDetails(userID):
    # Access DB
    database = connect_db()
    databaseCursor = database.cursor(pymysql.cursors.DictCursor)  # Use a DictCursor for named columns

    # Query the database for user details
    databaseCursor.execute(
        "SELECT * FROM Clients WHERE id = %s",
        (userID,)
    )

    user = databaseCursor.fetchone()
    # Close the database connection
    database.close()
    return user
#  Tickets
def insertTicket(name, revTag, eventID, amountDue, amountPaid, receiptID):
    database = connect_db()
    databaseCursor = database.cursor()

    databaseCursor.execute(
        "INSERT INTO Ticket (name, revTag, eventID, amountDue, amountPaid, receiptID) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, revTag, eventID, amountDue, amountPaid, receiptID)
    )
    database.commit()
    database.close()
    return json.dumps({"success": True})

def getTicketDetails(regID):
    # Access DB
    database = connect_db()
    databaseCursor = database.cursor(pymysql.cursors.DictCursor)  # Use a DictCursor for named columns

    # Query the database for registration details
    databaseCursor.execute(
        "SELECT * FROM Tickets WHERE id = %s",
        (regID,)
    ) 

    registration = databaseCursor.fetchone()
    # Close the database connection
    database.close()
    return registration

# Events
def insertEvent(eventName, max, price="", date=""):
    # Access DB
    database = connect_db()
    databaseCursor = database.cursor()

    # Insert a new event into the "events" table
    databaseCursor.execute(
        "INSERT INTO Event (name, max, price, date) VALUES (%d, %s, %s, %s, %s, %s)",
        (eventName, max, price, date)
    )

    # Save changes
    database.commit()
    database.close()
    return

def getEventDetails(eventID):
    # Access DB
    database = connect_db()
    databaseCursor = database.cursor(pymysql.cursors.DictCursor)  # Use a DictCursor for named columns

    # Query the database for registration details
    databaseCursor.execute(
        "SELECT * FROM Events WHERE id = %s",
        (eventID,)
    ) 

    registration = databaseCursor.fetchone()
    # Close the database connection
    database.close()
    return registration

def getEventIdJson(conn, eventID):
    database = connect_db()
    databaseCursor = database.cursor()
    databaseCursor.execute("SELECT eventID FROM Events WHERE id = %s", (eventID,))
    event = databaseCursor.fetchone()
    database.close()
    #return as json
    return json.dumps(event)  


# Queries:
# Check whether user has paid 
def hasPaid(db, event, user, bankStatement):
    databaseCursor = db.cursor()

    # Assuming 'event' table has columns 'registrant' and 'status'
    query = f"""
            SELECT Tickets, status FROM {event} WHERE name = '{user}' AND eventID = '{event}
    """
    databaseCursor.execute(query)
    result = databaseCursor.fetchone()

    if result:
        # If the user is found in the event table
        registrant_status = result[1]
        if user in bankStatement:
            # If the user is in the bankStatement array, set status to 'paid'
            if registrant_status != 'paid':
                databaseCursor.execute("UPDATE {event} SET status = 'paid' WHERE registrant = '{user}'")
                db.commit()
            else:
                print(f"User {user} is already marked as paid.")
        else:
            # If the user is not in the bankStatement array, set status to 'pending'
            if registrant_status != 'pending':
                databaseCursor.execute("UPDATE {event} SET status = 'pending' WHERE registrant = '{user}'")
                db.commit()
            else:
                print(f"User {user} is already marked as pending.")
    else:
        # If the user is not found in the event table, you might want to handle this case accordingly
        print(f"User {user} not found in the {event} table.")

# credentials: json
# "email": String
# "password": String
def validate_user(email, password):
    database = connect_db()
    databaseCursor = database.cursor()

    query = f"""
            SELECT * FROM Clients WHERE email = '{email}' AND password = '{password}'
    """
    databaseCursor.execute(query)
    result = databaseCursor.fetchone()

    if result:        
        return True
    else:
        return False
    
def session_add(email):
    database = connect_db()
    databaseCursor = database.cursor()

    expiry_date = int(time.time() + (24 * 60 * 60 * 7))

    token = jwt.encode({'email': email, 'expiryDate' : expiry_date}, str(current_app.config['JWT_SECRET_KEY']), algorithm="HS256")

    query = f"""
            INSERT INTO Sessions (token, client_email, expiry_date) VALUES ('{token}', '{email}', FROM_UNIXTIME('{expiry_date}'))
    """
    databaseCursor.execute(query)
    database.commit()
    database.close()

    return token, expiry_date

def query_db(connection, query, args=()):
    # Create a cursor object to execute SQL queries
    with connection.cursor() as cursor:
        # Execute the SQL query
        cursor.execute(query, args)
        # Return the results from the query
        return cursor.fetchall()
