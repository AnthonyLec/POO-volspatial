from tkinter import Toplevel, Label, Entry, Button, messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import uuid
from database import Database
from flight import Flight
from ui.helper import center_modal

class FlightPanelAdmin:
    def __init__(self, root, user_type, tree):
        self.root = root
        self.user_type = user_type
        self.tree = tree
        self.db = Database("db")
        self.button_frame = None 
        self.setup_buttons()
        self.load_data()

    def load_data(self):
        data = self.db.load("flights")
        self.current_data = data

        itineraries = {item['id']: item['name'] for item in self.db.load("itineraries")}
        vehicles = {item['id']: f"{item['model']} ({item['year_of_creation']})" for item in self.db.load("vehicles")}
        passengers = {item['id']: f"{item['last_name']} {item['first_name']}" for item in self.db.load("passengers")}
        pilots = {item['id']: f"{item['last_name']} {item['first_name']}" for item in self.db.load("pilots")}

        entities = []
        for item in data:
            entity = {
                "itinerary": itineraries[item['itinerary_id']],
                "vehicle": vehicles[item['vehicle_id']],
                "passengers": ', '.join([passengers[pid] for pid in item['passenger_ids']]),
                "pilot": pilots[item['pilot_id']],
                "date": item['date'],
                "notifications": item['notifications']
            }
            entities.append(entity)

        if not entities:
            return

        columns = list(entities[0].keys())
        rows = [list(entity.values()) for entity in entities]

        self.display_data(columns, rows)

    def display_data(self, columns, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        for row in rows:
            self.tree.insert("", "end", values=row)

        # self.tree.bind("<Double-1>", self.on_cell_double_click)

    def on_cell_double_click(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1
        current_value = self.tree.item(item, 'values')[column_index]

        def save_edited_value():
            new_value = entry.get()
            row_index = self.tree.index(item)
            self.current_data[row_index][list(self.current_data[row_index].keys())[column_index]] = new_value
            self.db.save("flights", self.current_data)
            self.load_data()
            edit_window.destroy()

        edit_window = Toplevel(self.root)
        edit_window.title("Edit Cell")
        entry = Entry(edit_window)
        entry.pack()
        entry.insert(0, current_value)
        save_button = Button(edit_window, text="Save", command=save_edited_value)
        save_button.pack()

    def setup_buttons(self):
        if self.button_frame is not None:
            self.button_frame.destroy()

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill="x")

        add_button = Button(self.button_frame, text="Add Flight", command=self.add_item)
        add_button.pack(side="left", padx=5, pady=5)

        delete_button = Button(self.button_frame, text="Delete Flight", command=self.delete_item)
        delete_button.pack(side="left", padx=5, pady=5)

    def add_item(self):
        def save_new_flight():
            itinerary_name = itinerary_combobox.get()
            vehicle_model = vehicle_combobox.get()
            pilot_name = pilot_combobox.get()

            itinerary_id = next(
                itinerary['id'] for itinerary in self.db.load("itineraries") if itinerary['name'] == itinerary_name)
            vehicle_id = next(vehicle['id'] for vehicle in self.db.load("vehicles") if
                              vehicle['model'] == vehicle_model.split(' ')[0])
            pilot_id = next(pilot['id'] for pilot in self.db.load("pilots") if
                            f"{pilot['last_name']} {pilot['first_name']}" == pilot_name)
            passenger_ids = []
            date_str = date_entry.get_date().strftime("%Y-%m-%d")

            new_flight = Flight(str(uuid.uuid4()), itinerary_id, vehicle_id, passenger_ids, pilot_id, date_str)
            self.current_data.append(new_flight.to_dict())
            self.db.save("flights", self.current_data)
            self.load_data()
            new_item_window.destroy()

        new_item_window = Toplevel(self.root)
        center_modal(new_item_window)
        new_item_window.title("Add Flight")

        Label(new_item_window, text="Itinerary").grid(row=0, column=0, padx=10, pady=5)
        itinerary_combobox = ttk.Combobox(new_item_window,
                                          values=[itinerary['name'] for itinerary in self.db.load("itineraries")])
        itinerary_combobox.grid(row=0, column=1, padx=10, pady=5)

        Label(new_item_window, text="Vehicle").grid(row=1, column=0, padx=10, pady=5)
        vehicle_combobox = ttk.Combobox(new_item_window,
                                        values=[f"{vehicle['model']} ({vehicle['year_of_creation']})" for vehicle in
                                                self.db.load("vehicles")])
        vehicle_combobox.grid(row=1, column=1, padx=10, pady=5)

        Label(new_item_window, text="Pilot").grid(row=2, column=0, padx=10, pady=5)
        pilot_combobox = ttk.Combobox(new_item_window, values=[f"{pilot['last_name']} {pilot['first_name']}" for pilot in
                                                               self.db.load("pilots")])
        pilot_combobox.grid(row=2, column=1, padx=10, pady=5)

        Label(new_item_window, text="Date").grid(row=3, column=0, padx=10, pady=5)
        date_entry = DateEntry(new_item_window, date_pattern='y-mm-dd')
        date_entry.grid(row=3, column=1, padx=10, pady=5)

        save_button = Button(new_item_window, text="Save", command=save_new_flight)
        save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a flight to delete")
            return

        selected_index = self.tree.index(selected_item[0])
        self.current_data.pop(selected_index)
        self.db.save("flights", self.current_data)
        self.load_data()
        messagebox.showinfo("Information", "Flight successfully deleted")

    def destroy(self):
        if self.button_frame is not None:
            self.button_frame.destroy()
            self.button_frame = None
