from Demos.win32ts_logoff_disconnected import username
from customtkinter import *
from tkinter import messagebox
from loginDataHandler import LoginHandler
from fontTools.misc.filenames import userNameToFileName

login_handler = LoginHandler()


def login():
    if usernameEntry.get()=='' or passwordEntry.get()=='':
        messagebox.showinfo('Error', 'Please enter your username and password')
    elif usernameEntry.get()=='nehir' and passwordEntry.get()=='123':
        messagebox.showinfo('Success', 'Login successful')
        root.destroy()
        import orderpage
    else:
        messagebox.showerror('Error','wrong credential')


def handle_login():
    username = usernameEntry.get()
    password = passwordEntry.get()

    # check credentials using the LoginHandler
    if login_handler.verify_credentials(username, password):
        messagebox.showinfo("Login Successful", "Welcome!")
        root.destroy()
        import orderpage
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")


root=CTk()
root.geometry('500x500')
root.resizable(False,False)
root.title('Pizza Ordering Site')

headinglabel=CTkLabel(root, text='Pizza Ordering Site',font=('Helvetica', 12, 'bold'))
headinglabel.place(x=195, y=100)

usernameEntry=CTkEntry(root,placeholder_text='Username',width=150)
usernameEntry.place(x=180, y=140)

passwordEntry=CTkEntry(root,placeholder_text='Password',width=150, show='*')
passwordEntry.place(x=180, y=180)

loginButton=CTkButton(root, text='Login',cursor='hand2',command=handle_login)
loginButton.place(x=185, y=230)




root.mainloop()