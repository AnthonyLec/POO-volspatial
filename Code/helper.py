def center_window(root):
   
    window_width = 1000
    window_height = 700
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False) 

    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

def center_modal(root):
    window_width = 400
    window_height = 200
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)  

    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)

    
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    root.title("Enter Passenger Info")
