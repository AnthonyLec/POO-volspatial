from tkinter import Toplevel, Label, Entry, Button, messagebox
from tkinter import ttk
import uuid
from database import Database
from pilot import Pilot
from ui.helper import center_modal

class PilotPanel:
    def __init__(self, root, user_type, tree):
        self.root = root
        self.user_type = user_type
        self.tree = tree
        self.db = Database("db")
        self.button_frame = None
        self.setup_buttons()
        self.load_data()

    def load_data(self):
        data = self.db.load("pilots")
        self.current_data = data
        entities = [Pilot.from_dict(item) for item in data]

        if not entities:
            return

        columns = list(entities[0].to_dict().keys())
        rows = [list(entity.to_dict().values()) for entity in entities]

        self.display_data(columns, rows)

    def display_data(self, columns, rows):
        self.tree.pack(fill="both", expand=True)

        for item in self.tree.get_children():
            self.tree.delete(item)

        
        column_mappings = {
            'last_name': 'Last Name',
            'first_name': 'First Name',
            'experience': 'Experience'
        }

        
        filtered_columns = [col for col in columns if col != 'id']
        renamed_columns = [column_mappings.get(col, col) for col in filtered_columns]
        filtered_rows = [[value for i, value in enumerate(row) if columns[i] != 'id'] for row in rows]

        self.tree["columns"] = renamed_columns
        self.tree["show"] = "headings"

        for col in renamed_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        for row in filtered_rows:
            self.tree.insert("", "end", values=row)

    def setup_buttons(self):
        if self.button_frame is not None:
            self.button_frame.destroy()

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill="x")

        add_button = Button(self.button_frame, text="Add Pilot", command=self.add_item)
        add_button.pack(side="left", padx=5, pady=5)

        delete_button = Button(self.button_frame, text="Delete Pilot", command=self.delete_item)
        delete_button.pack(side="left", padx=5, pady=5)

    def add_item(self):
        def save_new_item(fields):
            new_data = {field: entry.get() for field, entry in fields.items()}
            new_data['id'] = str(uuid.uuid4())
            new_item = Pilot.from_dict(new_data)
            self.current_data.append(new_item.to_dict())
            self.db.save("pilots", self.current_data)
            self.load_data()
            new_item_window.destroy()

        new_item_window = Toplevel(self.root)
        center_modal(new_item_window)
        new_item_window.title("Add Pilot")

        fields = {}
        labels = ["last_name", "first_name", "experience"]
        row = 0

        for label_text in labels:
            label = Label(new_item_window, text=label_text.capitalize())
            label.grid(row=row, column=0, padx=10, pady=5)
            entry = Entry(new_item_window)
            entry.grid(row=row, column=1, padx=10, pady=5)
            fields[label_text] = entry
            row += 1

        save_button = Button(new_item_window, text="Save", command=lambda: save_new_item(fields))
        save_button.grid(row=row, column=0, columnspan=2, pady=10)

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a pilot to delete")
            return

        selected_index = self.tree.index(selected_item[0])
        self.current_data.pop(selected_index)
        self.db.save("pilots", self.current_data)
        self.load_data()
        messagebox.showinfo("Information", "Pilot successfully deleted")

    def destroy(self):
        if self.button_frame is not None:
            self.button_frame.destroy()
            self.button_frame = None
