import tkinter as tk
from tkinter import Button
from tkinter import ttk
from ui.base_panel import BasePanel
from ui.passenger_panel import PassengerPanel
from ui.pilot_panel import PilotPanel
from ui.vehicle_panel import VehiclePanel
from ui.itinerary_panel import ItineraryPanel
from ui.flight_panel import FlightPanel
from ui.map_ui import MapUI
from ui.flight_panel_admin import FlightPanelAdmin

class App:
    def __init__(self, root, user_type):
        self.root = root
        self.root.title("Spacheflight Management")

        self.user_type = user_type

        self.current_panel = None 

        
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(side=tk.TOP, fill=tk.X)

        if self.user_type == "admin":
            self.create_button("Flights", self.load_flights_admin)
            self.create_button("Passengers", self.load_passengers)
            self.create_button("Pilots", self.load_pilots)
            self.create_button("Vehicles", self.load_vehicles)
            self.create_button("Bases", self.load_bases)
            self.create_button("Itineraries", self.load_itineraries)
            self.create_button("Map", self.show_map)

        
        self.tree = ttk.Treeview(root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.current_map = None

        
        if self.user_type != "admin":
            self.load_flights()

    def create_button(self, text, command):
        button = Button(self.buttons_frame, text=text, command=command)
        button.pack(side=tk.LEFT)

    def load_flights_admin(self):
        self.show_treeview()
        self.destroy_current_panel()
        self.current_panel = FlightPanelAdmin(self.root, self.user_type, self.tree)
        self.destroy_map()

    def load_flights(self):
        self.show_treeview()
        self.destroy_current_panel()
        self.current_panel = FlightPanel(self.root, self.user_type, self.tree)
        self.destroy_map()

    def load_passengers(self):
        self.show_treeview()
        self.destroy_current_panel()
        self.current_panel = PassengerPanel(self.root, self.user_type, self.tree)
        self.destroy_map()

    def load_pilots(self):
        self.show_treeview()
        self.destroy_current_panel()
        self.current_panel = PilotPanel(self.root, self.user_type, self.tree)
        self.destroy_map()

    def load_vehicles(self):
        self.show_treeview()
        self.destroy_current_panel()
        self.current_panel = VehiclePanel(self.root, self.user_type, self.tree)
        self.destroy_map()

    def load_bases(self):
        self.show_treeview()
        self.destroy_current_panel()
        self.current_panel = BasePanel(self.root, self.user_type, self.tree)
        self.destroy_map()

    def load_itineraries(self):
        self.show_treeview()
        self.destroy_current_panel()
        self.current_panel = ItineraryPanel(self.root, self.user_type, self.tree)
        self.destroy_map()

    def show_map(self):
        self.hide_treeview()
        self.destroy_map()
        self.destroy_current_panel()
        self.current_map = MapUI(self.root)

    def destroy_map(self):
        if self.current_map is not None:
            self.current_map.destroy()
            self.current_map = None

    def destroy_current_panel(self):
        if self.current_panel is not None:
            self.current_panel.destroy()
            self.current_panel = None

    def hide_treeview(self):
        self.tree.pack_forget()

    def show_treeview(self):
        self.tree.pack(fill=tk.BOTH, expand=True)
