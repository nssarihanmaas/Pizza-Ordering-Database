import datetime
from dataHandler import*
from mysql.connector import Error
from loginDataHandler import current_customer
from discountChecker import check_if_birthday



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

            global orderID
            orderID = cursor.fetchone()

            #Execute remaining queries
            for q in query:
                inserted_q = q % orderID[0]
                cursor.execute(inserted_q)

            #Update order price
            # fetch all orderitem rows
            fetch_all_items_query = "SELECT SUM(ItemPrice) AS price FROM orderitem WHERE OrderID = %s;"
            cursor.execute(fetch_all_items_query, orderID)

            result = cursor.fetchone()
            total = result[0]
            
            update_query = "UPDATE orderticket SET TotalPrice = %s WHERE OrderID = %s"
            values = (total, orderID[0])
            cursor.execute(update_query, values)

            # Apply discount if applicable 

            if(check_if_birthday()):
                discount_query = "UPDATE orderticket SET DiscountApplied = %s WHERE OrderID = %s"
                values = (10, orderID[0])
                cursor.execute(discount_query,values)

            connection.commit() 

        except Error as e:
            print(f"Error: {e}")
            # Rollback in case of error
            if connection.is_connected():
                connection.rollback()



