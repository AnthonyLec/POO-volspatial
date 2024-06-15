class Flight:
    def __init__(self, id, itinerary_id, vehicle_id, passenger_ids, pilot_id, date, notifications=None):
        self.id = id
        self.itinerary_id = itinerary_id
        self.vehicle_id = vehicle_id
        self.passenger_ids = passenger_ids
        self.pilot_id = pilot_id
        self.date = date
        self.notifications = notifications if notifications is not None else []

    def __repr__(self):
        return f"Flight(id={self.id}, itinerary_id={self.itinerary_id}, vehicle_id={self.vehicle_id}, passenger_ids={self.passenger_ids}, pilot_id={self.pilot_id}, date={self.date}, notifications={self.notifications})"

    def to_dict(self):
        return {
            'id': self.id,
            'itinerary_id': self.itinerary_id,
            'vehicle_id': self.vehicle_id,
            'passenger_ids': self.passenger_ids,
            'pilot_id': self.pilot_id,
            'date': self.date,
            'notifications': self.notifications
        }

    @staticmethod
    def from_dict(data):
        return Flight(
            data['id'],
            data['itinerary_id'],
            data['vehicle_id'],
            data['passenger_ids'],
            data['pilot_id'],
            data['date'],
            data.get('notifications', [])
        )
