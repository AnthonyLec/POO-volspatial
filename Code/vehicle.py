import uuid

class Vehicle:
    def __init__(self, id, model, capacity, year_of_creation):
        self.id = id
        self.model = model
        self.capacity = capacity
        self.year_of_creation = year_of_creation

    def __repr__(self):
        return f"Vehicle(id={self.id}, model={self.model}, capacity={self.capacity}, year_of_creation={self.year_of_creation})"

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Vehicle(data['id'], data['model'], data['capacity'], data['year_of_creation'])
