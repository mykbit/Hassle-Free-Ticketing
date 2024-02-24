from flask import current_app
import models

# TODO: Work on the structure of the tables
def create_clients():
    create_table_query = """
            CREATE TABLE IF NOT EXISTS Clients (
                email VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                
            )
            """
    models.query_db(current_app.db_connection, create_table_query, ())

