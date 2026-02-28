import json, os
from models import Bird

DB_FILE = "data/birds.json"

def load_birds():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_birds(birds):
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, "w") as f:
        json.dump(birds, f, indent=4)

def register_bird(name, species, anilha, father=None, mother=None):
    birds = load_birds()
    bird = Bird(name, species, anilha, father, mother)
    birds.append(bird.to_dict())
    save_birds(birds)
    return bird