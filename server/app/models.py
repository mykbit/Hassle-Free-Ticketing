import pymysql
import os

# Used to test the connection to the database from local environment, which allows bypass of Github Secrets
# from dotenv import load_dotenv

# Load environment variables from the .env file
# load_dotenv()

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

def query_db(connection, query, args=()):
    # Create a cursor object to execute SQL queries
    with connection.cursor() as cursor:
        # Execute the SQL query
        cursor.execute(query, args)
        # Return the results from the query
        return cursor.fetchall()
