from flask import current_app
import models


def create_events():
    create_event_table_query = """
            CREATE TABLE IF NOT EXISTS Events (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                max INT NOT NULL,
                price INT NOT NULL,
                date DATE,
                PRIMARY KEY (id)
            )
    """
    create_client_table_query = """
            CREATE TABLE IF NOT EXISTS Clients (
                id INT NOT NULL AUTO_INCREMENT
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                revTag VARCHAR(255),
                eventID INT NOT NULL,
                PRIMARY KEY (id)
            )
    """
    create_ticket_table_query = """
            CREATE TABLE IF NOT EXISTS Clients (
                id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                revTag VARCHAR(255),
                eventID INT NOT NULL,
                amountDue INT NOT NULL,
                amountPaid INT NOT NULL,
                receiptID INT,
                PRIMARY KEY (id)
            )
    """
    models.query_db(current_app.db_connection, create_event_table_query, ())
    models.query_db(current_app.db_connection, create_client_table_query, ())
    models.query_db(current_app.db_connection, create_ticket_table_query, ())