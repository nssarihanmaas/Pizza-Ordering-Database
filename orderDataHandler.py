import datetime
from dataHandler import*
from mysql.connector import Error
from loginDataHandler import currentCustomer


class orderHandlder:

    global query 
    query = []

    def clear_query(self):
        query.clear()
        # del query[1:]

    # def generateOrderTicket():
    #     customerID = current_customer
    #     #adds customer in one sql query

    #     # Prepare the INSERT statement
    #     base_query = """
    #         INSERT INTO orderticket (CustomerID, OrderDate, Status)
    #         VALUES (%s, %s, %s)
    #     """

    #     # Splitting the string at the first occurrence of %s
    #     parts = base_query.split('%s', 1)
    #     orderticket_query = parts[0] + str(customerID)  + parts[1]

    #     query.append(orderticket_query) 

    def addOrderItem(itemID, itemType, itemPrice):

        base_query = """
            INSERT INTO orderitem (OrderID, ItemType, ItemID, ItemPrice)
            VALUES(%s, %s, %s, %s)
        """
        parts = base_query.split('%s')

        item_query = parts[0] + '%s' + parts[1] + itemType + parts[2] + str(itemID) + parts[3] + str(itemPrice) + parts[4] 

        query.append(item_query)

    def placeOrder(self):
        
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
            
            # orderticket_query = query[0]
            # final_orderticket_queary = orderticket_query % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "Placed")
            # cursor.execute(final_orderticket_queary)

            # Retrieve the newly created orders id
            fetch_orderID_query = "SELECT OrderID FROM orderticket WHERE CustomerID = %s ORDER BY OrderDate DESC LIMIT 1;"
            cursor.execute(fetch_orderID_query, (customerID))

            orderID = cursor.fetchone()

            # Execute remaining queries
            for q in query[1:]:
                cursor.execute(q,orderID)
            
            connection.commit() 

        except Error as e:
            print(f"Error: {e}")
            # Rollback in case of error
            if connection.is_connected():
                connection.rollback()



