from customtkinter import*
import tkinter as tk
from tkinter import messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkComboBox
from connection import create_connection
from dataHandler import*
from orderHandler import*

window2=CTk()
window2.geometry('700x430')
window2.resizable(False,False)
window2.title('Order')

window2.mainloop()