from datetime import date
from dataHandler import*
from mysql.connector import Error
from loginDataHandler import current_customer

def check_if_birthday():


    customerID = current_customer
    connection = PizzaDataHandler().connection

    
    try:

        cursor = connection.cursor()

        # select the birthday column of the customer

        birthday_query = """SELECT Birthdate
        FROM customer
        WHERE CustomerID = %s;
        """
        cursor.execute(birthday_query,(customerID,))

        result = cursor.fetchone()
        birthdate = result[0]

        # get todays date

        today = date.today()

        # compare the two dates (without the year)

        if birthdate.month == today.month and birthdate.day == today.day:
            return True
        else:
            return False

    except Error as e:
        print(f"Error accessing database: {e}")