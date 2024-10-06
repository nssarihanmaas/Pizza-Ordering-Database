from customtkinter import*
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

orderPlacedLabel=CTkLabel(leftFrame2,text='Your Order Placed:',font=('Arial',18,'bold'),width=50)
orderPlacedLabel.grid(row=0,column=0,padx=10,pady=10)

orderPlacedText = tk.Text(leftFrame2, height=10, width=37, wrap="word")
orderPlacedText.grid(row=2, column=0, padx=10, pady=10)

orderPlacedText.insert(tk.END, f"Your order is placed")
orderPlacedText.insert(tk.END, "-"*37 + "\n")  # Divider line for clarity




deleteOrderButton=CTkButton(leftFrame2, text='Reset',cursor='hand2')
deleteOrderButton.grid(row=3,column=0,padx=30,pady=10)

window2.mainloop()