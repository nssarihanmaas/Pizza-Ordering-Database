from datetime import timedelta
from customtkinter import*
from customtkinter import *
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkComboBox
from connection import create_connection
from dataHandler import*
from orderHandler import*

window2=CTk()
window2.geometry('350x430')
window2.resizable(False,False)
window2.title('Order')

leftFrame2=CTkFrame(window2)
leftFrame2.grid(row=6,column=5)

orderPlacedText = tk.Text(leftFrame2, height=10, width=37, wrap="word")
orderPlacedText.grid(row=2, column=0, padx=10, pady=10)

orderPlacedText.insert(tk.END, f"Your order is placed")
orderPlacedText.insert(tk.END, "-"*33 + "\n")


def get_OrderDate(OrderID):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = "SELECT orderdate FROM orderticket WHERE OrderID = %s"
        cursor.execute(query, (OrderID,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else None
    else:
        print("Database connection failed.")
        return None

# Countdown function
def countdown(OrderID):
    OrderDate = get_OrderDate(OrderID)
    
    if OrderDate:
        # Add 5 minutes to the order time
        cancel_window_end = OrderDate + timedelta(minutes=5)
        current_time = OrderDate.now()
        time_remaining = int((cancel_window_end - current_time).total_seconds())
        
        if time_remaining > 0:
            minutes, seconds = divmod(time_remaining, 60)
            time_str = f'{minutes:02}:{seconds:02}'
            
            orderPlacedText.delete('1.0', tk.END)
            orderPlacedText.insert(tk.END, f"Your order is placed. \nTime remaining to cancel: {time_str}")

            window2.after(1000, lambda: countdown(OrderID))
        else:
            deleteOrderButton.grid_forget()
            orderPlacedText.insert(tk.END, "\nCancellation window closed.\n")
            orderPlacedText.insert(tk.END, "\nYour order is in process.\n")
    else:
        orderPlacedText.insert(tk.END, "\nOrder not found.\n")


orderPlacedLabel=CTkLabel(leftFrame2,text='Your Order Placed:',font=('Arial',18,'bold'),width=50)
orderPlacedLabel.grid(row=0,column=0,padx=10,pady=10)

deleteOrderButton=CTkButton(leftFrame2, text='Reset')
deleteOrderButton.grid(row=3,column=0,padx=30,pady=10)

window2.mainloop()