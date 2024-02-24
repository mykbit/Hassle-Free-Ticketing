from .models import query_db, connect_db


def create_tables():
    create_clients_table_query = """
            CREATE TABLE IF NOT EXISTS Clients (
                email       VARCHAR(255)    NOT NULL,
                password    VARCHAR(255)    NOT NULL,
                name        VARCHAR(255)    NOT NULL,
                PRIMARY KEY (email)
            );
    """

    create_events_table_query = """
            CREATE TABLE IF NOT EXISTS Events (
                id              INT             NOT NULL    AUTO_INCREMENT,
                name            VARCHAR(255)    NOT NULL,
                price           INT             NOT NULL,
                date            DATE            NOT NULL,
                holder_email    VARCHAR(255)    NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (holder_email) REFERENCES Clients(email)
            );
    """

    create_tickets_table_query = """
            CREATE TABLE IF NOT EXISTS Tickets (
                id              INT             NOT NULL    AUTO_INCREMENT,
                event_id        INT             NOT NULL,
                client_email    VARCHAR(255)    NOT NULL,
                valid           BOOLEAN         NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (event_id)      REFERENCES Events(id),
                FOREIGN KEY (client_email)  REFERENCES Clients(email)
            );
    """
    create_sessions_table_query = """
            CREATE TABLE IF NOT EXISTS Sessions (
                token           VARCHAR(255)    NOT NULL,
                client_email    VARCHAR(255)    NOT NULL,
                expiry_date     DATETIME        NOT NULL,      
                PRIMARY KEY (token),
                FOREIGN KEY (client_email)  REFERENCES Clients(email)
            );
    """
    query_db(connect_db(), create_clients_table_query, ())
    query_db(connect_db(), create_events_table_query, ())
    query_db(connect_db(), create_tickets_table_query, ())
    query_db(connect_db(), create_sessions_table_query, ())

