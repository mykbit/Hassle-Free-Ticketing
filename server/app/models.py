import pymysql
import os
import json

# Used to test the connection to the database from local environment, which allows bypass of Github Secrets
# from dotenv import load_dotenv

def init_db():
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


#   Insert Event into Database
#   Parameters:
#           eventID: ID for event. 
#           organiserID: ID of the person who created the event. (If our system allows for multiple users)
#           eventName: Name of event.
#           eventDate: Date range when event should be active
#           availableTickets: Number of tickets for event (default - 0)
def insertUser(json_input):
    data = json.loads(json_input)
    name = data['name']
    email = data['email']
    revolutTag = data['revolutTag']
    payment_status = data['payment_status']
    events = data['events']
    
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Insert a new user into the "users" table
    databaseCursor.execute(
        "INSERT INTO users (name, email, revolutTag, payment_status, event) VALUES (%s, %s, %s, %s, %s)",
        (name, email, revolutTag, payment_status, events)
    )

    # Save changes
    database.commit()
    database.close()
    return json.dumps({"success": True})



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

def insertUser(jsonInput):
    data = json.loads(jsonInput)
    name = data['name']
    email = data['email']
    revolutTag = data['revolutTag']
    payment_status = data['payment_status']
    events = data['events']
    database = init_db()
    databaseCursor = database.cursor()
    databaseCursor.execute(
        "INSERT INTO users (name, email, revolutTag, payment_status, event) VALUES (%s, %s, %s, %s, %s)",
        (name, email, revolutTag, payment_status, events)
    )

    # Save changes
    database.commit()
    database.close()
    return json.dumps({"success": True})


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


def updateUserName(jsonInput):
    data = json.loads(jsonInput)
    userID = data['userID']
    updatedName = data['updatedName']
    database = init_db()
    databaseCursor = database.cursor()
    databaseCursor.execute(
        "UPDATE users SET name = %s WHERE userID = %s",
        (updatedName, userID)
    )

    database.commit()
    database.close()
    return json.dumps({"success": True, "userID": userID, "updatedName": updatedName})

    
#   Insert Registration
#   Parameters:
#           registrationID: registrationID
#           userID: userID
#           eventID : eventID
#           registrationDate: date registered to event. 
#           paymentStatus: status of payment 

def insertRegistration(jsonInput):
    data = json.loads(jsonInput)
    registrationID = data['registrationID']
    userID = data['userID']
    eventID = data['eventID']
    registrationDate = data['registrationDate']
    paymentStatus = data['paymentStatus']
    database = init_db()
    databaseCursor = database.cursor()
    databaseCursor.execute(
        "INSERT INTO registrations (registrationID, userID, eventID, registrationDate, paymentStatus) VALUES (%s, %s, %s, %s, %s)",
        (registrationID, userID, eventID, registrationDate, paymentStatus)
    )
    database.commit()
    database.close()
    return json.dumps({"success": True})


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


def updateUser(jsonInput):
    data = json.loads(jsonInput)
    userID = data['userID']
    name = data['name']
    email = data['email']
    revolutTag = data['revolutTag']
    payment_status = data['payment_status']
    
    database = init_db()
    databaseCursor = database.cursor()
    databaseCursor.execute(
        "UPDATE users SET name = %s, email = %s, revolutTag = %s, payment_status = %s WHERE userID = %s",
        (name, email, revolutTag, payment_status, userID)
    )
    database.commit()
    database.close()
    return json.dumps({"success": True, "userID": userID, "updatedInfo": {"name": name, "email": email, "revolutTag": revolutTag, "payment_status": payment_status}})



def getEventIdJson(conn, eventID):
    database = init_db()
    databaseCursor = database.cursor()
    databaseCursor.execute("SELECT eventID FROM events WHERE eventID = %s", (eventID,))
    event = databaseCursor.fetchone()
    database.close()
    #return as json
    return json.dumps(event)  


# Check whether user has paid by going through registrants in an event and check to see if the 
# registant is in bankStatement (Array for now)
# If entry exists we set the status of the transaction as paid.
# Needs to be updated for child tables  
def hasPaid(db, event, user, bankStatement):
    databaseCursor = db.cursor()

    # Assuming 'event' table has columns 'registrant' and 'status'
    query = f"""
            SELECT registrant, status FROM {event} WHERE registrant = '{user}'
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

# # Test
# event_table_name = "your_event_table_name"
# user_to_check = "user_to_check"
# bank_statement = ["user1", "user2", "user3"]  # Replace with your actual bank statement array
# hasPaid(db, event_table_name, user_to_check, bank_statement)


# credentials: json
# "email": String
# "password": String
def validate_user(credentials):
    inputDict = json.loads(credentials)
    database = init_db()
    databaseCursor = database.cursor()

    query = f"""
            SELECT * FROM organisation WHERE email = '{inputDict['password']}'
    """
    databaseCursor.execute(query)
    result = databaseCursor.fetchone()

    if result:
        # If the email is found in the organisation table
        password_column_index = databaseCursor.column_names.index('password')
        stored_password = result[password_column_index]
        
        if inputDict['password'] == stored_password:
            print("Credentials are valid.")
            return True
        else:
            print("Password does not match.")
            return False
    else:
        # If the email is not found in the organisation table
        print("Email not found.")
        return False

def saveEvent(organisationID, eventName, link, description="", capacity="", date=""):
    # Access DB
    database = init_db()
    databaseCursor = database.cursor()

    # Insert a new event into the "events" table
    databaseCursor.execute(
        "INSERT INTO event (organisationID, eventName, link, description, capacity, date) VALUES (%d, %s, %s, %s, %s, %s)",
        (organisationID, eventName, link, description, capacity, date)
    )

    # Save changes
    database.commit()
    database.close()
    return


def query_db(connection, query, args=()):
    # Create a cursor object to execute SQL queries
    with connection.cursor() as cursor:
        # Execute the SQL query
        cursor.execute(query, args)
        # Return the results from the query
        return cursor.fetchall()

def insertUser(json_input):
    data = json.loads(json_input)
    email = data['email']
    password = data['password']
    name = data['name']
    revTag = data.get('revTag', "")  
    eventID = data.get('eventID', "")
    database = init_db()
    databaseCursor = database.cursor()
    databaseCursor.execute(
        "INSERT INTO users (email, password, name, revTag, eventID) VALUES (%s, %s, %s, %s, %s)",
        (email, password, name, revTag, eventID)
    )
    database.commit()
    database.close()
    return json.dumps({"success": True})
