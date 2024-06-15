import tkinter as tk
from tkinter import ttk
from database import Database
import random
import json
import uuid
from datetime import datetime

class MapUI:
    def __init__(self, parent):
        self.parent = parent
        self.db = Database("db")
        self.obstacle = None  
        self.current_flight_id = None
        self.create_ui()

    def create_ui(self):
        self.create_frame()
        self.create_combobox()
        self.create_canvas()
        self.draw_initial_map()

    def create_frame(self):
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)

    def create_combobox(self):
        self.combobox_frame = tk.Frame(self.frame)
        self.combobox_frame.pack(side=tk.TOP, fill=tk.X)
        self.flight_combobox = ttk.Combobox(self.combobox_frame, values=self.get_flight_ids())
        self.flight_combobox.pack(side=tk.TOP, fill=tk.X)
        self.flight_combobox.bind("<<ComboboxSelected>>", self.on_flight_selected)

    def create_canvas(self):
        self.map_canvas = tk.Canvas(self.frame, width=400, height=400)
        self.map_canvas.pack(fill=tk.BOTH, expand=True)
        self.map_canvas.bind("<Configure>", self.resize_canvas)

    def draw_initial_map(self):
        self.map_canvas.delete("all")
        # Ensure the canvas is empty initially

    def draw_map(self):
        self.map_canvas.delete("all")
        base_coords = self.get_base_coordinates()
        self.draw_itineraries(base_coords)
        self.draw_bases(base_coords)

    def get_flight_ids(self):
        return [flight['id'] for flight in self.db.load("flights")]

    def get_base_coordinates(self):
        bases = self.db.load("bases")
        return {base['id']: (int(base['x']), int(base['y'])) for base in bases}

    def draw_itineraries(self, base_coords):
        itineraries = self.db.load("itineraries")
        for itinerary in itineraries:
            base_ids = itinerary['base_ids']
            for i in range(len(base_ids) - 1):
                self.draw_line(base_coords, base_ids[i], base_ids[i + 1], color='red')

    def draw_line(self, base_coords, base_id1, base_id2, color):
        x1, y1 = base_coords[base_id1]
        x2, y2 = base_coords[base_id2]
        self.map_canvas.create_line(x1, y1, x2, y2, fill=color)
        self.add_obstacle(x1, y1, x2, y2)

    def add_obstacle(self, x1, y1, x2, y2):
        t = 0.5 + 0.5 * random.random() 
        ox = x1 + t * (x2 - x1)
        oy = y1 + t * (y2 - y1)
        self.obstacle = self.map_canvas.create_rectangle(ox - 5, oy - 5, ox + 5, oy + 5, fill='black')

    def draw_bases(self, base_coords):
        for base_id, (x, y) in base_coords.items():
            self.draw_base(x, y, base_id)

    def draw_base(self, x, y, base_id):
        self.map_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill='blue')
        base_name = self.get_base_name(base_id)
        self.map_canvas.create_text(x, y - 10, text=base_name, anchor=tk.S)

    def get_base_name(self, base_id):
        bases = self.db.load("bases")
        return next(base['name'] for base in bases if base['id'] == base_id)

    def on_flight_selected(self, event):
        flight_id = self.flight_combobox.get()
        self.current_flight_id = flight_id
        selected_flight = self.get_selected_flight(flight_id)
        self.display_flight_on_map(selected_flight)

    def get_selected_flight(self, flight_id):
        return next(flight for flight in self.db.load("flights") if flight['id'] == flight_id)

    def display_flight_on_map(self, flight):
        self.map_canvas.delete("all")
        base_coords = self.get_base_coordinates()
        itinerary = self.get_flight_itinerary(flight['itinerary_id'])
        self.draw_flight_path(base_coords, itinerary)
        self.draw_bases_in_itinerary(base_coords, itinerary['base_ids'])
        self.animate_vehicle(base_coords, itinerary['base_ids'])

    def get_flight_itinerary(self, itinerary_id):
        return next(it for it in self.db.load("itineraries") if it['id'] == itinerary_id)

    def draw_flight_path(self, base_coords, itinerary):
        base_ids = itinerary['base_ids']
        for i in range(len(base_ids) - 1):
            self.draw_line(base_coords, base_ids[i], base_ids[i + 1], color='green')

    def draw_bases_in_itinerary(self, base_coords, base_ids):
        for base_id in base_ids:
            x, y = base_coords[base_id]
            self.draw_base(x, y, base_id)

    def animate_vehicle(self, base_coords, base_ids):
        if len(base_ids) < 2:
            return
        x1, y1 = base_coords[base_ids[0]]
        self.vehicle = self.map_canvas.create_rectangle(x1 - 8, y1 - 8, x1 + 8, y1 + 8, fill='red')
        self.move_vehicle(self.vehicle, base_coords, base_ids, 0)

    def move_vehicle(self, vehicle, base_coords, base_ids, i):
        if i >= len(base_ids) - 1:
            return
        x1, y1 = base_coords[base_ids[i]]
        x2, y2 = base_coords[base_ids[i + 1]]
        dx = (x2 - x1) / 50
        dy = (y2 - y1) / 50
        self.animate_step(vehicle, dx, dy, i, base_coords, base_ids, 0)

    def animate_step(self, vehicle, dx, dy, i, base_coords, base_ids, step):
        if step > 50:
            self.move_vehicle(vehicle, base_coords, base_ids, i + 1)
            return
        self.map_canvas.move(vehicle, dx, dy)
        self.parent.update()
        if self.check_collision(vehicle):
            self.handle_collision(vehicle)
        self.parent.after(100, self.animate_step, vehicle, dx, dy, i, base_coords, base_ids, step + 1)

    def check_collision(self, vehicle):
        vehicle_coords = self.map_canvas.coords(vehicle)
        overlap = self.map_canvas.find_overlapping(*vehicle_coords)
        return self.obstacle in overlap

    def handle_collision(self, vehicle):
        self.create_explosion()
        self.map_canvas.delete(self.obstacle)
        self.obstacle = None
        # Add notification to the flight database
        vehicle_coords = self.map_canvas.coords(vehicle)
        self.add_notification(vehicle_coords)

    def add_notification(self, coords):
        flight = self.get_selected_flight(self.current_flight_id)
        notification = f"An obstacle has been hit at coordinates {coords}."
        flight["notifications"].append(notification)
        self.update_flight_in_db(flight)
        self.display_message(notification)

    def update_flight_in_db(self, updated_flight):
        flights = self.db.load("flights")
        for idx, flight in enumerate(flights):
            if flight['id'] == updated_flight['id']:
                flights[idx] = updated_flight
                break
        self.db.save("flights", flights)

    def display_message(self, message):
        message_id = self.map_canvas.create_text(400, 100, text=message, fill='red', font=('Helvetica', 16))
        self.parent.update()
        self.parent.after(3000, lambda: self.map_canvas.delete(message_id))

    def create_explosion(self):
        explosion_coords = self.map_canvas.coords(self.obstacle)
        x1, y1, x2, y2 = explosion_coords
        explosion = self.map_canvas.create_oval(x1 - 10, y1 - 10, x2 + 10, y2 + 10, fill='orange', outline='yellow')
        self.parent.update()
        self.parent.after(500, lambda: self.map_canvas.delete(explosion))

    def resize_canvas(self, event):
        self.draw_initial_map()

    def destroy(self):
        self.frame.destroy()
