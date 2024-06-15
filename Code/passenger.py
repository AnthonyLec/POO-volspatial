import uuid

class Passenger:
    def __init__(self, id, last_name, first_name, age, reserved_flights=None):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.age = age
        self.reserved_flights = reserved_flights or []

    def __repr__(self):
        return f"Passenger(id={self.id}, last_name={self.last_name}, first_name={self.first_name}, age={self.age}, reserved_flights={self.reserved_flights})"

    def to_dict(self):
        return {
            'id': self.id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'age': self.age,
            'reserved_flights': self.reserved_flights
        }

    @staticmethod
    def from_dict(data):
        return Passenger(data['id'], data['last_name'], data['first_name'], data['age'], data.get('reserved_flights', []))
