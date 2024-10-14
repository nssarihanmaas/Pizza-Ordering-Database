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

def check_if_11th_order():

    customerID = current_customer
    connection = PizzaDataHandler().connection

    try:
        cursor = connection.cursor()

         # select the birthday column of the customer

        count_query = "SELECT pizza_order_count FROM discount WHERE customer_id = %s;"
    
        cursor.execute(count_query, (customerID,))

        result = cursor.fetchone()
        count =  result[0]

        if count > 9:
            return True

        return False
    except Error as e:
        print(f"Error accessing database: {e}")
    