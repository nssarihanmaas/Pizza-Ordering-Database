from datetime import timedelta
from customtkinter import*
from customtkinter import *
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkComboBox
from connection import create_connection
from dataHandler import*
from orderHandler import*
from orderHandler import orderID

window3=CTk()
window3.geometry('350x350')
window3.resizable(False,False)
window3.title('Delivery Tracker')

leftFrame3=CTkFrame(window3)
leftFrame3.grid(row=6,column=6)

progressText = tk.Text(leftFrame3, height=10, width=37, wrap="word")
progressText.grid(row=2, column=0, padx=10, pady=10)

progressText.insert(tk.END, f"Your order is in progress.")
progressText.insert(tk.END, f"\nDelivery Person: ---")

orderPlacedLabel=CTkLabel(leftFrame3,text='Progress Summary:',font=('Arial',18,'bold'),width=50)
orderPlacedLabel.grid(row=0,column=0,padx=10,pady=10)

def update():

    connection = PizzaDataHandler().connection

    try:

        cursor = connection.cursor()

        #check if orderID exists in the deliveryassignemt table
        assignment_query = "SELECT * FROM deliveryassignment WHERE OrderID = %s;"
        cursor.execute(assignment_query, orderID)
        result = cursor.fetchone()

        assignee = "---"

        if result is not None:
            assignee_id = result[1]
            
            # Select the assignee name

            cursor.execute("SELECT Name FROM deliveryperson WHERE DeliveryPersonID = %s;", (assignee_id,))
            result = cursor.fetchone()
            assignee = result[0]

        #update status
        # Clear the text box and insert the new status
        progressText.delete(1.0, tk.END)
        progressText.insert(tk.END, f"Your order is in progress.")
        progressText.insert(tk.END, f"\nDelivery Person: " + assignee)
    
        # Schedule the next update in 5 seconds (5000 milliseconds)
        window3.after(5000, update)
        #update delivery assigment
        
    except Error as e:
        print(f"Error accessing database: {e}")


update()

window3.mainloop()