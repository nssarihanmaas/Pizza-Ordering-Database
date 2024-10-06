from customtkinter import *
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkComboBox
from connection import create_connection
from dataHandler import *
from orderHandler import *

def countdown(time_remaining):
    minutes, seconds = divmod(time_remaining, 60)
    time_str = f'{minutes:02}:{seconds:02}'
    
    orderPlacedText.delete('1.0', tk.END)
    orderPlacedText.insert(tk.END, f"Your order is placed. \nTime remaining to cancel: {time_str}")

    if time_remaining > 0:
        window2.after(1000, countdown, time_remaining - 1)
    else:
        deleteOrderButton.grid_forget()
        orderPlacedText.insert(tk.END, "\nCancellation window closed.\n")
        orderPlacedText.insert(tk.END, "\nYour order is in process.\n")

window2 = CTk()
window2.geometry('350x430')
window2.resizable(False, False)
window2.title('Order')

leftFrame2 = CTkFrame(window2)
leftFrame2.grid(row=6, column=5)

orderPlacedLabel = CTkLabel(leftFrame2, text='Your Order Placed:', font=('Arial', 18, 'bold'), width=50)
orderPlacedLabel.grid(row=0, column=0, padx=10, pady=10)

orderPlacedText = tk.Text(leftFrame2, height=10, width=37, wrap="word")
orderPlacedText.grid(row=2, column=0, padx=10, pady=10)

orderPlacedText.insert(tk.END, f"Your order is placed\n")
orderPlacedText.insert(tk.END, "-" * 37 + "\n")

def cancel():
    orderHandlder.deleteOrder()

countdown(3)

deleteOrderButton=CTkButton(leftFrame2, text='Reset',cursor='cancel')
deleteOrderButton.grid(row=3,column=0,padx=30,pady=10)

window2.mainloop()
