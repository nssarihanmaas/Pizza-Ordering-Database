import datetime
from dataHandler import*
from mysql.connector import Error
from loginDataHandler import *


class orderHandlder:

    global query 
    query = []

    def clear_query():
        query.clear()

    def addOrderItem(itemID, itemType, itemPrice):

        base_query = """
            INSERT INTO orderitem (OrderID, ItemType, ItemID, ItemPrice)
            VALUES(%s, %s, %s, %s)
        """
        parts = base_query.split('%s')

        item_query = parts[0] + '%s' + parts[1] + itemType + parts[2] + str(itemID) + parts[3] + str(itemPrice) + parts[4] 
        
        query.append(item_query)


    def placeOrder():
        
        customerID = current_customer
        connection = PizzaDataHandler().connection

        try:

            cursor = connection.cursor()

            # Create the order ticket so the order id can be used to create order item relations

            ticket_query = """
                INSERT INTO orderticket (CustomerID, OrderDate, Status)
                VALUES (%s, %s, %s)
            """
            values = (customerID, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Placed')
            cursor.execute(ticket_query,values)

            # Retrieve the newly created orders id
            fetch_orderID_query = "SELECT OrderID FROM orderticket WHERE CustomerID = " + str(customerID) + " ORDER BY OrderDate DESC LIMIT 1;"
            cursor.execute(fetch_orderID_query)

            
            orderID = cursor.fetchone()

            #Execute remaining queries
            for q in query:
                inserted_q = q % orderID[0]
                cursor.execute(inserted_q)
            
            connection.commit() 

        except Error as e:
            print(f"Error: {e}")
            # Rollback in case of error
            if connection.is_connected():
                connection.rollback()

    
    def deleteOrder():

        customerID = current_customer
        connection = PizzaDataHandler().connection

        try:
            cursor = connection.cursor()

            fetch_orderID_query = "SELECT OrderID FROM orderticket WHERE CustomerID = " + str(customerID) + " ORDER BY OrderDate DESC LIMIT 1;"
            cursor.execute(fetch_orderID_query)
            orderID = cursor.fetchone()

            item_deletion_query ="DELETE FROM orderitem WHERE OrderID = " + str(orderID[0]) +" ;"
            ticket_deletion_query ="DELETE FROM orderticket WHERE OrderID = " + str(orderID[0]) +" ;"
            cursor.execute(item_deletion_query)
            cursor.execute(ticket_deletion_query)

            connection.commit() 
        except Error as e:
            print(f"Error: {e}")
            # Rollback in case of error
            if connection.is_connected():
                connection.rollback()






