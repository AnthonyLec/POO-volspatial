from tkinter import Toplevel, Label, Button, Entry, messagebox
import tkinter as tk
from tkinter import ttk
import random
from database import Database
from flight import Flight
from passenger import Passenger
from ui.helper import center_modal


class FlightPanel:
    def __init__(self, root, user_type, tree):
        self.root = root
        self.user_type = user_type
        self.tree = tree
        self.db = Database("db")
        self.passenger_entity = None
        self.initialize_ui()

    def initialize_ui(self):
        self.load_flights_data()
        self.create_buttons_frame()
        self.create_passenger_flights_table()

    def load_flights_data(self):
        flights_data = self.db.load("flights")
        itinerary_data = {item['id']: item['name'] for item in self.db.load("itineraries")}
        vehicle_data = {item['id']: (item['model'], item['year_of_creation']) for item in self.db.load("vehicles")}
        pilot_data = {item['id']: f"{item['last_name']} {item['first_name']}" for item in self.db.load("pilots")}

        entities = [Flight.from_dict(item) for item in flights_data]

        if entities:
            columns_mapping = {
                "itinerary_id": "Itinerary",
                "vehicle_id": "Vehicle",
                "pilot_id": "Pilot",
                "date": "Date",
                "notifications": "Notifications"
            }
            columns = [columns_mapping.get(col, col) for col in entities[0].to_dict().keys() if
                       col not in ["id", "passenger_ids"]]
            rows = [
                [
                    (itinerary_data[value] if key == "itinerary_id" else
                     f"{vehicle_data[value][0]} ({vehicle_data[value][1]})" if key == "vehicle_id" else
                     pilot_data[value] if key == "pilot_id" else value)
                    for key, value in entity.to_dict().items() if key not in ["id", "passenger_ids"]
                ]
                for entity in entities
            ]
            self.display_data(self.tree, columns, rows)

    def display_data(self, tree, columns, rows):
        tree.pack(fill="both", expand=True)
        tree.delete(*tree.get_children())
        tree["columns"] = columns
        tree["show"] = "headings"

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for row in rows:
            tree.insert("", "end", values=row)

    def create_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=10)

        self.passenger_modal_button = Button(self.buttons_frame, text="Login", command=self.open_passenger_modal,
                                             font=('Helvetica', 12, 'bold'), bg='#4CAF50', fg='black', padx=10, pady=5, borderwidth=3)
        self.passenger_modal_button.pack(side=tk.LEFT, padx=10)

        self.reserve_button = Button(self.buttons_frame, text="Reserve Flight", command=self.open_reserve_modal,
                                     font=('Helvetica', 12, 'bold'), bg='#4CAF50', fg='black', padx=10, pady=5, borderwidth=3)
        self.reserve_button.pack(side=tk.LEFT, padx=10)

    def open_passenger_modal(self):
        self.passenger_modal = Toplevel(self.root)

        center_modal(self.passenger_modal)
        self.passenger_modal.title("Login")

        Label(self.passenger_modal, text="Last Name").pack(pady=5)
        self.last_name_entry = Entry(self.passenger_modal)
        self.last_name_entry.pack(pady=5)

        Label(self.passenger_modal, text="First Name").pack(pady=5)
        self.first_name_entry = Entry(self.passenger_modal)
        self.first_name_entry.pack(pady=5)

        Button(self.passenger_modal, text="Submit", command=self.submit_passenger_info).pack(pady=10)

    def submit_passenger_info(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        passenger_data = self.db.load("passengers")
        passenger = next((p for p in passenger_data if p['last_name'] == last_name and p['first_name'] == first_name), None)

        if passenger is None:
            messagebox.showerror("Error", "Passenger not found.")
        else:
            self.passenger_entity = Passenger.from_dict(passenger)
            messagebox.showinfo("Success", "Passenger found and loaded.")
            self.create_passenger_flights_table()

        self.passenger_modal.destroy()

    def create_passenger_flights_table(self):
        if not self.passenger_entity:
            return

        reserved_flight_ids = self.passenger_entity.reserved_flights
        flights_data = self.db.load("flights")
        itinerary_data = {item['id']: item['name'] for item in self.db.load("itineraries")}
        vehicle_data = {item['id']: (item['model'], item['year_of_creation']) for item in self.db.load("vehicles")}
        pilot_data = {item['id']: f"{item['last_name']} {item['first_name']}" for item in self.db.load("pilots")}

        reserved_flights = [Flight.from_dict(flight) for flight in flights_data if flight['id'] in reserved_flight_ids]

        if reserved_flights:
            columns_mapping = {
                "itinerary_id": "Itinerary",
                "vehicle_id": "Vehicle",
                "pilot_id": "Pilot",
                "date": "Date",
                "notifications": "Notifications"
            }
            columns = [columns_mapping.get(col, col) for col in reserved_flights[0].to_dict().keys() if
                       col not in ["id", "passenger_ids"]]
            rows = [
                [
                    (itinerary_data[value] if key == "itinerary_id" else
                     f"{vehicle_data[value][0]} ({vehicle_data[value][1]})" if key == "vehicle_id" else
                     pilot_data[value] if key == "pilot_id" else value)
                    for key, value in flight.to_dict().items() if key not in ["id", "passenger_ids"]
                ]
                for flight in reserved_flights
            ]

            if hasattr(self, 'tree_reserved'):
                self.tree_reserved.destroy()

            self.tree_reserved = ttk.Treeview(self.root)
            self.display_data(self.tree_reserved, columns, rows)
            self.tree_reserved.pack(fill="both", expand=True)

    def open_reserve_modal(self):
        if not self.passenger_entity:
            messagebox.showwarning("No Passenger", "Please enter passenger info first.")
            return

        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No selection", "Please select a flight to reserve.")
            return

        flight_data = self.tree.item(selected_item)['values']
        flight_index = self.tree.index(selected_item) 
        flight_id = self.db.load("flights")[flight_index]['id']  

        if flight_id in self.passenger_entity.reserved_flights:
            messagebox.showwarning("Already Reserved", "This flight is already reserved.")
            return

        self.modal = Toplevel(self.root)
        center_modal(self.modal)
        self.modal.title("Confirm Reservation")

        price = random.randint(100, 1000)
        self.price_label = Label(self.modal, text=f"Price: ${price}")
        self.price_label.pack(pady=10)

        self.confirm_button = Button(self.modal, text="Confirm",
                                     command=lambda: self.confirm_reservation(flight_id, price))
        self.confirm_button.pack(pady=10)

    def confirm_reservation(self, flight_id, price):
        passenger_id = self.passenger_entity.id
        passenger_data = self.db.load("passengers")
        passenger = next((p for p in passenger_data if p['id'] == passenger_id), None)

        if not passenger:
            messagebox.showerror("Error", "Passenger not found.")
            return

        passenger['reserved_flights'].append(flight_id)
        self.db.save("passengers", passenger_data)
        self.passenger_entity = Passenger.from_dict(passenger)

        self.update_flight_passenger_list(flight_id, passenger_id)

        messagebox.showinfo("Success", f"Flight {flight_id} reserved for ${price}")
        self.modal.destroy()

        
        self.create_passenger_flights_table()

    def update_flight_passenger_list(self, flight_id, passenger_id):
        flights_data = self.db.load("flights")
        flight = next((f for f in flights_data if f['id'] == flight_id), None)

        if not flight:
            messagebox.showerror("Error", "Flight not found.")
            return

        if passenger_id not in flight['passenger_ids']:
            flight['passenger_ids'].append(passenger_id)
            self.db.save("flights", flights_data)
