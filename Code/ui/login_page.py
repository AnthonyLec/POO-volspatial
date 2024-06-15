import tkinter as tk
from tkinter import Button, Entry, Label, Toplevel, messagebox
import json
from ui.app_ui import App

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.customer_button = Button(self.frame, text="Customer", command=self.customer_login,
                                    font=('Helvetica', 14, 'bold'), bg='#4CAF50', fg='black', padx=40, pady=20, borderwidth=3)
        self.customer_button.pack(pady=20)

        self.admin_button = Button(self.frame, text="Admin", command=self.admin_login,
                                   font=('Helvetica', 14, 'bold'), bg='#4CAF50', fg='black', padx=40, pady=20, borderwidth=3)
        self.admin_button.pack(pady=20)

    def customer_login(self):
        self.frame.destroy()
        App(self.root, "customer")

    def admin_login(self):
        self.admin_password_window = Toplevel(self.root)
        self.admin_password_window.title("Admin Login")

        self.put_window_in_center()

        Label(self.admin_password_window, text="Password").pack(pady=5)
        self.password_entry = Entry(self.admin_password_window, show="*")
        self.password_entry.pack(pady=5)
        Button(self.admin_password_window, text="Login", command=self.check_admin_password,
               font=('Helvetica', 12), bg='#4CAF50', fg='black', padx=10, pady=5, borderwidth=2).pack(pady=10)

    def put_window_in_center(self):
       
        window_width = 300
        window_height = 200
        self.admin_password_window.geometry(f"{window_width}x{window_height}")
        self.admin_password_window.resizable(False, False)  

        
        screen_width = self.admin_password_window.winfo_screenwidth()
        screen_height = self.admin_password_window.winfo_screenheight()

       
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)

        
        self.admin_password_window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    def check_admin_password(self):
        with open("db/admin_passwords.json", "r") as file:
            passwords = json.load(file)

        if self.password_entry.get() in passwords["passwords"]:
            self.admin_password_window.destroy()
            self.frame.destroy()
            App(self.root, "admin")
        else:
            messagebox.showerror("Error", "Incorrect Password")
