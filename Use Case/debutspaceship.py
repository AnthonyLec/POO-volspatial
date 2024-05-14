class Spaceship:
    def __init__(self, ID, type, max_passengers, range_fuel, max_speed, shape, licence_required, weight):
        self.ID = ID
        self.type = type
        self.max_passengers = max_passengers
        self.range_fuel = range_fuel
        self.max_speed = max_speed
        self.shape = shape
        self.licence_required = licence_required
        self.weight = weight

    def __str__(self):
        return f"Spaceship {self.ID}: Type - {self.type}, Max Passengers - {self.max_passengers}, Range - {self.range_fuel} km, Max Speed - {self.max_speed} km/h, Shape - {self.shape}, Licence Required - {self.licence_required}, Weight - {self.weight} tons"
        
    def check_pilot_licence(self, pilot):
        if pilot.licence_type == self.licence_required:
            print(f"Pilot {pilot.ID} has the required licence ({self.licence_required}) to pilot this spaceship.")
            return True
        else:
            print(f"Pilot {pilot.ID} does not have the required licence ({self.licence_required}) to pilot this spaceship.")
            return False


class Pilot:
    def __init__(self, ID, licence_type):
        self.ID = ID
        self.licence_type = licence_type

    def __str__(self):
        return f"Pilot {self.ID}: Licence Type - {self.licence_type}"

