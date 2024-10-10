import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='CemresuAkman1996**',
            database='pizzaorders'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
