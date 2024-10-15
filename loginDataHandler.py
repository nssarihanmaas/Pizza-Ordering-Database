import tkinter as tk
import tkinter.messagebox as messagebox
from customtkinter import CTk, CTkButton, CTkComboBox, CTkFrame
from connection import create_connection

class LoginHandler:
    def __init__(self):
        
        self.connection = create_connection()
        if self.connection is None:
            messagebox.showerror("Connection Error", "Failed to connect to the database.")
        else:
            self.cursor = self.connection.cursor()

    def verify_credentials(self, username, password):
        """Checks the users credentials against the database records"""
        try:
            
            self.cursor.execute("SELECT * FROM Customer WHERE Name = %s AND Password = %s", (username, password))
            result = self.cursor.fetchone()
            
            
            global current_customer
            current_customer = result[0]

            return result is not None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while verifying credentials: {str(e)}")
            return False

    def close_connection(self):
        
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()