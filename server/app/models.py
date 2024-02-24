import pymysql
import os

def init_db():
    db_host = os.environ.get('DATABASE_HOST')
    db_port = int(os.environ.get('DATABASE_PORT', 3306))
    db_user = os.environ.get('DATABASE_USER')
    db_password = os.environ.get('DATABASE_PASSWORD')
    db_name = os.environ.get('DATABASE_NAME')
    return pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name,
    )

def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS temp_table (
                userID INT AUTO_INCREMENT PRIMARY KEY,
                firstName VARCHAR(255),
                lastName VARCHAR(255),
                emailAddress VARCHAR(255),
                amountPaid DECIMAL(10, 2),
                eventName VARCHAR(255)
            )
        """)
    conn.commit()

def insert_data(conn, table, data):
    with conn.cursor() as cursor:
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join([f"`{key}`" for key in data.keys()])
        sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, list(data.values()))
    conn.commit()

def select_data(conn, table, columns='*', condition=None):
    with conn.cursor() as cursor:
        sql = f"SELECT {columns} FROM `{table}`" + (f" WHERE {condition}" if condition else "")
        cursor.execute(sql)
        return cursor.fetchall()

def update_data(conn, table, data, condition):
    with conn.cursor() as cursor:
        updates = ', '.join([f"`{k}` = %s" for k in data.keys()])
        sql = f"UPDATE `{table}` SET {updates} WHERE {condition}"
        cursor.execute(sql, list(data.values()))
    conn.commit()

def delete_data(conn, table, condition):
    with conn.cursor() as cursor:
        sql = f"DELETE FROM `{table}` WHERE {condition}"
        cursor.execute(sql)
    conn.commit()

# this just example guys
    
if __name__ == "__main__":
    conn = init_db()
    create_table(conn)  # Create the table
    # Example operations
    insert_data(conn, 'temp_table', {
        'firstName': 'AnandJR',
        'lastName': 'Anand',
        'emailAddress': 'anandanand@example.com',
        'amountPaid': 1000.00,
        'eventName': 'Hackathon'
    })
    print(select_data(conn, 'temp_table'))
    update_data(conn, 'temp_table', {'amountPaid': 149.99}, "userID = 1")
    print(select_data(conn, 'temp_table', condition="userID = 1"))
    delete_data(conn, 'temp_table', "userID = 1")
    print(select_data(conn, 'temp_table'))
    conn.close()
