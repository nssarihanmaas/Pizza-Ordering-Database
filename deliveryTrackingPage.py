from datetime import datetime, timedelta
import traceback
from customtkinter import *
import tkinter as tk
from connection import create_connection
from dataHandler import *
from orderHandler import *
from orderHandler import orderID

window3 = CTk()
window3.geometry('350x350')
window3.resizable(False, False)
window3.title('Delivery Tracker')

leftFrame3 = CTkFrame(window3)
leftFrame3.grid(row=6, column=6)

progressText = tk.Text(leftFrame3, height=10, width=37, wrap="word")
progressText.grid(row=2, column=0, padx=10, pady=10)

progressText.insert(tk.END, f"Your order is in progress.")

orderPlacedLabel = CTkLabel(leftFrame3, text='Progress Summary:', font=('Arial', 18, 'bold'), width=50)
orderPlacedLabel.grid(row=0, column=0, padx=10, pady=10)

def update():
    connection = PizzaDataHandler().connection

    try:
        cursor = connection.cursor()

        # Check if orderID exists in the deliveryassignment table
        assignment_query = "SELECT * FROM deliveryassignment WHERE OrderID = %s;"
        cursor.execute(assignment_query, orderID)
        result = cursor.fetchone()

        assignee = "We will assign a delivery person shortly..."

        if result is None:
            # No delivery person assigned yet, fetch customer area code
            customer_query = """
                SELECT c.areaCode 
                FROM orderticket o 
                JOIN customer c ON o.CustomerID = c.CustomerID 
                WHERE o.OrderID = %s;
            """
            cursor.execute(customer_query, orderID)
            customer_area = cursor.fetchone()[0]

            # Find a delivery person assigned to the same area and check last_order time
            delivery_person_query = """
                SELECT DeliveryPersonID, last_order 
                FROM deliveryperson 
                WHERE PostalCodeArea = %s;
            """
            cursor.execute(delivery_person_query, (customer_area,))
            delivery_persons = cursor.fetchall()

            for delivery_person in delivery_persons:
                delivery_person_id, last_order = delivery_person

                # Check if 30 minutes have passed since the last order
                if last_order is None or (datetime.datetime.now() - last_order >= timedelta(minutes=30)) or (datetime.datetime.now() - last_order <= timedelta(minutes=3)):
                    # Insert the assignment into the deliveryassignment table
                    insert_assignment = "INSERT INTO deliveryassignment (OrderID, DeliveryPersonID) VALUES (%s, %s);"
                    cursor.execute(insert_assignment, (orderID[0], delivery_person_id))
                    connection.commit()

                    # Update the last_order time
                    update_last_order = "UPDATE deliveryperson SET last_order = NOW() WHERE DeliveryPersonID = %s;"
                    cursor.execute(update_last_order, (delivery_person_id,))
                    connection.commit()

                    # Retrieve the assignee name
                    cursor.execute("SELECT Name FROM deliveryperson WHERE DeliveryPersonID = %s;", (delivery_person_id,))
                    assignee = cursor.fetchone()[0]

                    break  # Exit the loop after assigning a delivery person

        else:
            assignee_id = result[1]

            # Select the assignee name
            cursor.execute("SELECT Name FROM deliveryperson WHERE DeliveryPersonID = %s;", (assignee_id,))
            result = cursor.fetchone()
            assignee = result[0]

        # Update status
        # Clear the text box and insert the new status
        progressText.delete(1.0, tk.END)
        progressText.insert(tk.END, f"Your order is in progress.")
        progressText.insert(tk.END, f"\nDelivery Person: " + assignee)

        # Schedule the next update in 5 seconds (5000 milliseconds)
        window3.after(5000, update)

    except Error as e:
        print(f"Error accessing database: {e}")
        traceback.print_exc()

update()

window3.mainloop()
