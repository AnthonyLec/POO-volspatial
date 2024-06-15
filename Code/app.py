import tkinter as tk
from database import Database
from ui.helper import center_window
from ui.login_page import LoginPage

if __name__ == "__main__":
    db = Database("db")
    

    window = tk.Tk()
    center_window(window)

    LoginPage(window)
    window.mainloop()
