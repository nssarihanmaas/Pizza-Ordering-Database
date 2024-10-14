from datetime import timedelta
import importlib
from customtkinter import*
from customtkinter import *
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkComboBox
from connection import create_connection
from dataHandler import*
from orderHandler import*
from orderHandler import orderID

window2=CTk()
window2.geometry('350x430')
window2.resizable(False,False)
window2.title('Order')

leftFrame2=CTkFrame(window2)
leftFrame2.grid(row=6,column=5)

orderPlacedText = tk.Text(leftFrame2, height=10, width=37, wrap="word")
orderPlacedText.grid(row=2, column=0, padx=10, pady=10)

def reset_order():
    
    conn = create_connection()  
    cursor = conn.cursor()

    # Update iscancelled field in the orderticket table
    query_cancel_order = "UPDATE orderticket SET IsCancelled = TRUE WHERE orderID = %s"
    cursor.execute(query_cancel_order, orderID)
    conn.commit()
    
    # Inform the user that the order has been cancelled
    orderPlacedText.insert(tk.END, f"Your order has been cancelled.\n")
    orderPlacedText.insert(tk.END, "-"*31 + "\n")
    
    # Close the cursor and connection after the query
    cursor.close()
    conn.close()

def terminate_and_import():
    # Import the new file here
    # Replace 'new_file_name' with the actual name of the file you want to import
    window2.destroy()
    import deliveryTrackingPage


# Schedule the termination and import after 5 minutes (300,000 milliseconds)
window2.after(3000, terminate_and_import)

orderPlacedText.insert(tk.END, f"Your order is placed")
orderPlacedText.insert(tk.END, "-"*33 + "\n")

orderPlacedLabel=CTkLabel(leftFrame2,text='Your Order Placed:',font=('Arial',18,'bold'),width=50)
orderPlacedLabel.grid(row=0,column=0,padx=10,pady=10)

deleteOrderButton=CTkButton(leftFrame2, text='Reset', command=reset_order)
deleteOrderButton.grid(row=3,column=0,padx=30,pady=10)

window2.mainloop()