import uuid
from datetime import date

class Bird:
    def __init__(self, name, species, anilha, father=None, mother=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.species = species
        self.anilha = anilha
        self.father = father
        self.mother = mother
        self.registered_on = date.today().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "anilha": self.anilha,
            "father": self.father,
            "mother": self.mother,
            "registered_on": self.registered_on
        }