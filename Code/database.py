import json
from base import Base
from pilot import Pilot
from passenger import Passenger
from vehicle import Vehicle
from itinerary import Itinerary
from flight import Flight
import os
import uuid


class Database:
    def __init__(self, db_folder):
        self.db_folder = db_folder
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)

    def _get_file_path(self, entity_name):
        return os.path.join(self.db_folder, f"{entity_name}.json")

    def load(self, entity_name):
        file_path = self._get_file_path(entity_name)
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as file:
            return json.load(file)

    def save(self, entity_name, data):
        file_path = self._get_file_path(entity_name)
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def add(self, entity_name, item):
        data = self.load(entity_name)
        data.append(item)
        self.save(entity_name, data)

    def update(self, entity_name, index, item):
        data = self.load(entity_name)
        if 0 <= index < len(data):
            data[index] = item
            self.save(entity_name, data)

    def delete(self, entity_name, index):
        data = self.load(entity_name)
        if 0 <= index < len(data):
            data.pop(index)
            self.save(entity_name, data)

