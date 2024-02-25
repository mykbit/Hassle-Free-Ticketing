import sys
from flask import current_app, jsonify
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



    user = databaseCursor.fetchone()
    # Close the database connection
    database.close()
    return user
#  Tickets

def insertTicket(eventID, email, valid=True):
    database = connect_db()
    with database.cursor() as cursor:
        cursor.execute(
            "INSERT INTO Tickets (event_id, client_email, valid) VALUES (%s, %s, %s)",
            (eventID, email, valid)
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
def insertEvent(name, price, date, holder_email):
    # Access DB
    database = connect_db()
    databaseCursor = database.cursor()
        # Insert a new event into the "Events" table
    databaseCursor.execute(
            "INSERT INTO Events (name, price, date, holder_email) VALUES (%s, %s, %s, %s)",
            (name, price, date, holder_email)
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

def getEventIdJson(eventID):
    database = connect_db()
    databaseCursor = database.cursor(pymysql.cursors.DictCursor)  # Use a DictCursor for named columns
    databaseCursor.execute("SELECT * FROM Events WHERE id = %s", (eventID,))
    event = databaseCursor.fetchone()
    database.close()
    # Return as json
    return json.dumps(event)


# Queries:
# Check whether user has paid 
def hasPaid(email, event_id):
    db = connect_db()
    databaseCursor = db.cursor()

    # Use parameterized queries to avoid SQL injection
    query = "SELECT valid FROM Tickets WHERE client_email = %s AND event_id = %s"
    databaseCursor.execute(query, (email, event_id))
    result = databaseCursor.fetchone()

    return result;

def get_registration(event_id, email):
    database = connect_db()
    databaseCursor = database.cursor()  # Use a DictCursor for named columns
    databaseCursor.execute("SELECT * FROM Tickets WHERE event_id = %s AND client_email = %s", (event_id, email))
    result = databaseCursor.fetchone()
    database.close()
    if result:
        return True
    else:
        return False

# credentials: json
# "email": String
# "password": String
def validate_credentials(email, password):
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

def create_event_db(name, price, date, holder_email):
    database = connect_db()
    databaseCursor = database.cursor()

    query = f"""
            INSERT INTO Events (name, price, date, holder_email) VALUES ('{name}', '{price}', '{date}', '{holder_email}')
    """
    databaseCursor.execute(query)
    database.commit()
    databaseCursor.execute("SELECT * from Events WHERE id = LAST_INSERT_ID()")
    result = databaseCursor.fetchone()
    database.close()

    return result

def check_token(token):
    database = connect_db()
    databaseCursor = database.cursor()

    query = """
            SELECT client_email FROM Sessions WHERE token = %s
    """
    databaseCursor.execute(query, (token,))
    result = databaseCursor.fetchone()

    database.close()

    if result:
        return result[0]  # Return the first column of the result
    else:
        return False

def getClient(email):
    # Access DB
    database = connect_db()
    databaseCursor = database.cursor()  # Use a DictCursor for named columns

    # Query the database for user details
    databaseCursor.execute(
        "SELECT * FROM Clients WHERE email = %s",
        (email,)
    )

    res = databaseCursor.fetchone()

    return res


def query_db(connection, query, args=()):
    # Create a cursor object to execute SQL queries
    with connection.cursor() as cursor:
        # Execute the SQL query
        cursor.execute(query, args)
        # Return the results from the query
        return cursor.fetchall()

def get_latest():
    database = connect_db()
    databaseCursor = database.cursor()

    query = f"""
        SELECT timestamp FROM Payments
        ORDER BY timestamp DESC
        LIMIT 1 ;
    """
    databaseCursor.execute(query)
    result = databaseCursor.fetchone()
    return result

def validate_payment(transfers, event_id):
    database = connect_db()
    databaseCursor = database.cursor()

    for transfer in transfers:
        query = f"""
            SELECT price FROM Events WHERE id='{event_id}';
        """
        databaseCursor.execute(query)
        result = databaseCursor.fetchone()
        ticket2validate = int(float(transfer['Amount']) / result[0])

        print(ticket2validate, file=sys.stderr)

        name = transfer['Description'].replace("FROM ", "")
    
        query = f"""
            UPDATE Tickets AS t 
            JOIN (SELECT id
                FROM Tickets AS t2
                JOIN Clients AS c2 ON t2.client_email = c2.email
                WHERE c2.name = '{name}' AND t2.valid IS FALSE
                LIMIT {ticket2validate}) AS sub
            ON t.id = sub.id
            SET t.valid = TRUE;
        """

        databaseCursor.execute(query)
        database.commit()
        result = databaseCursor.fetchone()

        query = f"""
            INSERT INTO Payments (timestamp, description, amount)
            VALUES ('{transfer['timestamp']}', '{transfer['Description']}', {int(float(transfer['Amount']))});
        """
        databaseCursor.execute(query)
        database.commit()
