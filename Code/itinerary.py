class Itinerary:
    def __init__(self, id, name, base_ids):
        self.id = id
        self.name = name
        self.base_ids = base_ids

    def __repr__(self):
        return f"Itinerary(id={self.id}, name={self.name}, base_ids={self.base_ids})"

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'base_ids': self.base_ids}

    @staticmethod
    def from_dict(data):
        return Itinerary(data['id'], data['name'], data['base_ids'])
