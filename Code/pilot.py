import uuid

class Pilot:
    def __init__(self, id, last_name, first_name, experience):
        self.id = id
        self.last_name = last_name
        self.first_name = first_name
        self.experience = experience

    def __repr__(self):
        return f"Pilot(id={self.id}, last_name={self.last_name}, first_name={self.first_name}, experience={self.experience})"

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Pilot(data['id'], data['last_name'], data['first_name'], data['experience'])
