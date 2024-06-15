import uuid

class Base:
    def __init__(self, id, name, location, x, y):
        self.id = id
        self.name = name
        self.location = location
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Base(id={self.id}, name={self.name}, location={self.location}, x={self.x}, y={self.y})"

    def to_dict(self):
        return {
                'id': self.id,
                'name': self.name,
                'location': self.location,
                'x': self.x,
                'y': self.y
                }

    @staticmethod
    def from_dict(data):
        return Base(data['id'], data['name'], data['location'], data['x'], data['y'])

